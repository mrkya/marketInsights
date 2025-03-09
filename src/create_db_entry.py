# create_db_entry.py
from bs4 import BeautifulSoup
import time as time_module

# global variables for content extraction
author_key = "byline-attr-author"
time_key = "byline-attr-time-style"
author_meta_key = "byline-attr-meta-separator"
time_key_1 = "datetime"
time_key_2 = "data-timestamp"  
content_key = "atoms-wrapper"   

def fetch_metadata(soup):
    # Find and print all <div> elements with the class name "byline"
    author_divs = soup.find_all("div", class_=author_key)
    authors = [div.text.strip() for div in author_divs]

    # Find all <div> elements with the class name "byline-attr-time-style"
    time_divs = soup.find_all("div", class_=time_key)
    time_stamps = []
    for div in time_divs:
        time_elem = div.find("time")
        time_stamp = (time_elem.get(time_key_1) or time_elem.get(time_key_2))
        if time_stamp:
            time_stamps.append(time_stamp)

    return {
        "authors": authors,
        "time_stamp": time_stamps[0] if len(time_stamps) > 0 else None
    }

def fetch_content(soup):
    paragraphs = []
    content_divs = soup.find_all("div", class_=content_key) 
    for content_div in content_divs:
        p_tags = content_div.find_all("p")
        for p in p_tags:
            paragraphs.append(p.text.strip())

    return paragraphs

def create_db_entry(title, url, driver):
    # Load the specified URL
    driver.get(url)
    time_module.sleep(3)  # Allow time for content to load

    # Extract Page Source
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    meta_data = fetch_metadata(soup)
    article_paragraphs = fetch_content(soup)

    return {
        "title": title,
        "url": url,
        "authors": meta_data["authors"],
        "time_stamp": meta_data["time_stamp"],
        "content": article_paragraphs   
    }
    