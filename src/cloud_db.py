import psycopg2
import json
from google.cloud import secretmanager

# Function to retrieve database credentials from Google Secret Manager
def get_db_config():
    client = secretmanager.SecretManagerServiceClient()
    secret_name = "projects/856075255563/secrets/db-connect/versions/latest"
    print("✅ Fetching secret...")  
    # Access the secret
    response = client.access_secret_version(request={"name": secret_name})
    secret_payload = response.payload.data.decode("UTF-8")
    return json.loads(secret_payload)


# Function to establish connection
def connect():
    try:
        conn = psycopg2.connect(**get_db_config())
        cursor = conn.cursor()
        print("✅ Successfully connected to Google Cloud SQL PostgreSQL!")
        return conn, cursor
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None, None

# SQL statements history 
# SELECT * FROM financial_news;
# TRUNCATE TABLE financial_news;
# CREATE TABLE IF NOT EXISTS financial_news (
#    id SERIAL PRIMARY KEY,
#    title TEXT NOT NULL,
#    url TEXT UNIQUE NOT NULL,
#    authors TEXT[],
#    timestamp TIMESTAMP NOT NULL,
#    content TEXT,
#    summary TEXT,
#    sentiment_score FLOAT
#);
