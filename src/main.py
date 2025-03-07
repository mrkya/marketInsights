# main.py    
from fetch_metadata import fetch_metadata
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re

def main():
    global done
    done = False

    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode for efficiency
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    server=Service(ChromeDriverManager().install()) 
    driver = webdriver.Chrome(service=server,options=options)

    # Load Yahoo Finance News Page
    url = "https://finance.yahoo.com/topic/latest-news/"
    driver.get(url)

    time.sleep(3)  # Allow time for content to load
    
    # Extract Page Source
    soup = BeautifulSoup(driver.page_source, "html.parser") 

    # Find news headlines
    news_data = []
    headlines = soup.find_all("h3")

    for h in headlines:  # Fetch top 10 headlines
        title = h.text.strip()
        a_tag = h.find_previous("a")
        link = a_tag["href"] if a_tag and "href" in a_tag.attrs else None
        if link and re.search(r'/news/.', link):
            news_data.append({"title": title, "link": link})

    # Print extracted news
    for news in news_data[:3]:
        fetch_metadata(news["title"], news["link"], driver) 
        
    # Close WebDriver
    driver.quit()

if __name__ == "__main__":
    main()