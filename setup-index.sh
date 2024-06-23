#!/bin/bash

# Wait for Elasticsearch to be ready
echo "Waiting for Elasticsearch to be ready..."

# Define the Elasticsearch URL
ELASTICSEARCH_URL=${ELASTICSEARCH_URL:-"http://localhost:9200"}

# Create an index
echo "Creating index..."
curl -X PUT "${ELASTICSEARCH_URL}/documents" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text"
      },
      "date": {
        "type": "date"
      },
      "content": {
        "type": "text"
      }
    }
  }
}
'

# Index sample documents
echo "Indexing sample documents..."

# Financial documents
curl -X POST "${ELASTICSEARCH_URL}/documents/_doc" -H 'Content-Type: application/json' -d'
{
  "title": "Global Market Overview",
  "date": "2024-06-23",
  "content": "The global markets have experienced significant volatility over the past quarter. Key drivers include changes in interest rates, geopolitical tensions, and emerging market dynamics. Investors are advised to diversify their portfolios to mitigate risks. The S&P 500 saw a 3% decline while the Nasdaq experienced a 2% increase."
}
'

curl -X POST "${ELASTICSEARCH_URL}/documents/_doc" -H 'Content-Type: application/json' -d'
{
  "title": "Quarterly Financial Report",
  "date": "2024-03-31",
  "content": "Our company reported a 5% increase in revenue this quarter, driven by strong sales in the North American market. Operating expenses remained flat, resulting in a 10% increase in net income. The board has approved a new stock buyback program."
}
'

# Law documents
curl -X POST "${ELASTICSEARCH_URL}/documents/_doc" -H 'Content-Type: application/json' -d'
{
  "title": "Supreme Court Ruling on Data Privacy",
  "date": "2024-05-15",
  "content": "The Supreme Court has issued a landmark ruling on data privacy, establishing new guidelines for how companies must handle personal information. The ruling mandates stricter consent requirements and increased transparency in data usage. Legal experts predict widespread impacts across various industries."
}
'

curl -X POST "${ELASTICSEARCH_URL}/documents/_doc" -H 'Content-Type: application/json' -d'
{
  "title": "Contract Law: Recent Developments",
  "date": "2024-04-10",
  "content": "Recent developments in contract law have focused on the enforceability of digital agreements. Courts have increasingly upheld the validity of electronic signatures and online contracts, provided that parties have clearly expressed their consent and intention to be bound by such agreements."
}
'

# Tech documents
curl -X POST "${ELASTICSEARCH_URL}/documents/_doc" -H 'Content-Type: application/json' -d'
{
  "title": "AI Advancements in 2024",
  "date": "2024-06-20",
  "content": "Artificial intelligence continues to advance at a rapid pace, with significant breakthroughs in natural language processing and autonomous systems. Leading tech companies have introduced new AI-driven products that promise to enhance productivity and drive innovation across various sectors."
}
'

curl -X POST "${ELASTICSEARCH_URL}/documents/_doc" -H 'Content-Type: application/json' -d'
{
  "title": "Cybersecurity Threats: An Overview",
  "date": "2024-06-18",
  "content": "Cybersecurity remains a critical concern as cyberattacks become more sophisticated. Recent incidents have highlighted the vulnerabilities in critical infrastructure and the importance of robust security measures. Organizations are urged to adopt a proactive approach to cybersecurity, including regular risk assessments and employee training."
}
'

echo "Setup complete."
