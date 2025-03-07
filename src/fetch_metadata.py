# fetch_metadata.py
from bs4 import BeautifulSoup
import time as time_module
import json

author_key = "byline-attr-author"
time_key = "byline-attr-time-style"
author_meta_key="byline-attr-meta-separator"
time_key_1 = "datetime"
time_key_2 = "data-timestamp"  

def fetch_metadata(title, url, driver):
    # Load the specified URL
    driver.get(url)
    time_module.sleep(3)  # Allow time for content to load

    # Extract Page Source
    soup = BeautifulSoup(driver.page_source, "html.parser")

    meta_data = []
    
    # Find and print all <div> elements with the class name "byline"
    author_divs = soup.find_all("div", class_=author_key)
    authors = [div.text.strip() for div in author_divs]

    # Find all <div> elements with the class name "byline-attr-time-style"
    time_divs = soup.find_all("div", class_=time_key)
    time_stamps = []
    for div in time_divs:
        time_elem = div.find("time")
        time_stamp = time_elem.get(time_key_1) if time_elem.get(time_key_1) else time_elem.get(time_key_2)  
        if time_elem:
            time_stamps.append(time_stamp)

    meta_data.append({  
        "title": title,
        "url": url,
        "authors": authors,
        "time_stamps": time_stamps[0]
    })
    
    # Pretty-print the meta_data array
    print(json.dumps(meta_data, indent=4))

    return soup