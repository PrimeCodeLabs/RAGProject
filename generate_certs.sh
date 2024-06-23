#!/bin/bash

# Define directories
CERT_DIR=certificates
ES_CERTS_DIR=$CERT_DIR/elasticsearch

# Create directories
mkdir -p $ES_CERTS_DIR

# Generate CA key and certificate
openssl genpkey -algorithm RSA -out $CERT_DIR/ca-key.pem
openssl req -x509 -new -nodes -key $CERT_DIR/ca-key.pem -sha256 -days 3650 -out $CERT_DIR/ca-cert.pem -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=example.com"

# Generate Elasticsearch key and certificate signing request (CSR)
openssl genpkey -algorithm RSA -out $ES_CERTS_DIR/elasticsearch-key.pem
openssl req -new -key $ES_CERTS_DIR/elasticsearch-key.pem -out $ES_CERTS_DIR/elasticsearch.csr -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=elasticsearch"

# Sign the Elasticsearch certificate with the CA
openssl x509 -req -in $ES_CERTS_DIR/elasticsearch.csr -CA $CERT_DIR/ca-cert.pem -CAkey $CERT_DIR/ca-key.pem -CAcreateserial -out $ES_CERTS_DIR/elasticsearch-cert.pem -days 365 -sha256

# Create a PKCS12 keystore
openssl pkcs12 -export -out $ES_CERTS_DIR/elasticsearch-keystore.p12 -inkey $ES_CERTS_DIR/elasticsearch-key.pem -in $ES_CERTS_DIR/elasticsearch-cert.pem -certfile $CERT_DIR/ca-cert.pem -password pass:changeit

# Convert the PKCS12 keystore to a JKS keystore
keytool -importkeystore -deststorepass changeit -destkeypass changeit -destkeystore $ES_CERTS_DIR/elasticsearch-keystore.jks -srckeystore $ES_CERTS_DIR/elasticsearch-keystore.p12 -srcstoretype PKCS12 -srcstorepass changeit

# Import the CA certificate to the Elasticsearch truststore
keytool -import -file $CERT_DIR/ca-cert.pem -alias "ca" -keystore $ES_CERTS_DIR/elasticsearch-truststore.jks -storepass changeit -noprompt

echo "Certificates generated in the $CERT_DIR directory."
