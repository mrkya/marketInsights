import psycopg2
from config import db_config

# Create a table to store news articles 
def create_table(cursor, conn): 
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS news_articles (
                id SERIAL PRIMARY KEY,
                title TEXT,
                url TEXT,
                authors TEXT,
                timestamp TIMESTAMP,
                content TEXT,
                summary TEXT,
                sentiment_score FLOAT
            );
        """)
        conn.commit()
        print("✅ Table created successfully!")
    except Exception as e:
        print(f"❌ Error creating table: {e}")

# Store news article in the database    
def store_article(cursor, conn, article):
    try:
        cursor.execute("""
            INSERT INTO news_articles (title, url, authors, timestamp, content)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING;  -- Avoid duplicate inserts
        """, (article["title"], article["url"], article["authors"], article["timestamp"], article["content"]))
        conn.commit()
        print(f"✅ Saved: {article['title']}")
    except Exception as e:
        print(f"❌ Error saving article: {e}")


# Create a connection to the database and runs a give action
# article can be generalized to payload if needed   
def create_connection(action, article=None):    
    actions = {
        "create_table": create_table,
        "store_article": store_article  
    }

    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        actions[action](cursor, conn, article)  # Call the specified action
        print("✅ Successfully connected to AWS RDS PostgreSQL!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        
    