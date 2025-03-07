from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import threading
import itertools
import sys
import re

def animate():
    green_color = '\033[92m'
    reset_color = '\033[0m'
    sys.stdout.write('\n')
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write(f'\r{green_color}Loading {c}{reset_color}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\n')
    sys.stdout.write(f'\r{green_color}Done!{reset_color}\n')


def main():
    global done
    done = False

    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode for efficiency
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Start the animation in a separate thread
    t = threading.Thread(target=animate)
    t.start()

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

    # Stop the animation
    done = True
    t.join()

    for h in headlines:  # Fetch top 10 headlines
        title = h.text.strip()
        a_tag = h.find_previous("a")
        link = a_tag["href"] if a_tag and "href" in a_tag.attrs else None
        if link and re.search(r'/news/.', link):
            news_data.append({"title": title, "link": link})

    # Close WebDriver
    driver.quit()

   # Print extracted news
    for news in news_data:
        print(f"Title: {news['title']}")
        print(f"Link: {news['link']}\n")

if __name__ == "__main__":
    main()