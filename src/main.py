# main.py    
from create_db_entry import create_db_entry
from cloud_db import connect
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re

url = "https://finance.yahoo.com/topic/latest-news/"

def main():
    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode for efficiency
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Initialize the Chrome WebDriver   
    server=Service(ChromeDriverManager().install()) 
    driver = webdriver.Chrome(service=server,options=options)

    # Load Yahoo Finance News Page
    driver.get(url)

    print("✅ Scraping web...")
    time.sleep(3)  # Allow time for content to load
    soup = BeautifulSoup(driver.page_source, "html.parser") # Extract Page Source
    
    # Find all news headlines
    news_data = []
    headlines = soup.find_all("h3")

    # Extract news title and link   
    for h in headlines:
        title = h.text.strip()
        a_tag = h.find_previous("a")
        link = a_tag["href"] if a_tag and "href" in a_tag.attrs else None
        if link and re.search(r'/news/.', link):
            news_data.append({"title": title, "link": link})
    
    # Connect to the database   
    conn, cursor = connect()        

    # Print extracted news
    for news in news_data[:1]:
        record = create_db_entry(news["title"], news["link"], driver)  
        if conn and cursor:
            try:
                cursor.execute("""
                    INSERT INTO financial_news (title, url, authors, timestamp, content, summary, sentiment_score)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, record)
                conn.commit()
                print("✅ Sample data inserted successfully!")
            except Exception as e:
                print(f"❌ Error inserting data: {e}")
        
    # Close WebDriver
    driver.quit()
    cursor.close()
    conn.close()
    print("✅ Connection closed.")

if __name__ == "__main__":
    main()