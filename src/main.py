from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode for efficiency
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

server=Service(ChromeDriverManager().install()) 
driver = webdriver.Chrome(service=server,options=options)

# Load Yahoo Finance News Page
url = "https://finance.yahoo.com"
driver.get(url)
time.sleep(3)  # Allow time for content to load

# Extract Page Source
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find news headlines
news_data = []
headlines = soup.find_all("h3")

for h in headlines[:10]:  # Fetch top 10 headlines
    title = h.text.strip()
    a_tag = h.find("a")
    link = a_tag["href"] if a_tag and "href" in a_tag.attrs else None
    if link:
        full_link = f"https://finance.yahoo.com{link}" if link.startswith("/") else link
        news_data.append({"title": title, "link": full_link})

# Close WebDriver
driver.quit()

# Print extracted news
for news in news_data:
    print(f"Title: {news['title']}")
    print(f"Link: {news['link']}\n")
