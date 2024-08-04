import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import re
import json
import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

#1. Run the script for the first time: When you run the script for the first time, it will open WhatsApp Web and prompt you to log in by scanning the QR code.
#2. Subsequent runs: On subsequent runs, the script will use the saved session data from the custom user data directory, and you should not need to log in again unless the session expires.

# Specify the path to your custom user data directory
user_data_dir = "C:/Users/Usuario/AppData/Local/Google/Chrome/User Data/Default"
chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
#chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
time.sleep(2)
driver.get("https://web.whatsapp.com")
time.sleep(20)
print("whatsapp is open!")

parent_elements = driver.find_elements(By.CLASS_NAME, "x10l6tqk.xh8yej3.x1g42fcv")
print(len(parent_elements))
list = []

for element in parent_elements:
    #print(element.text)
    html_content = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')
    #image_url = soup.find('img')['src']
    #title = soup.find('span', {'dir': 'auto'}).get('title', '')
    name = soup.find('span', {'dir': 'auto'}).text
    chat_time = soup.find('div', class_='_ak8i').text
    soup_txt = soup.find('span', class_='x78zum5 x1cy8zhl')
    text = soup_txt.text if soup_txt else ''
    #txt2 = link_span.get('title', '') if link_span else ''
    soup_messages = soup.find('span', class_='x1rg5ohu x173ssrc x1xaadd7 x682dto x1e01kqd x12j7j87 x9bpaai x1pg5gke x1s688f xo5v014 x1u28eo4 x2b8uid x16dsc37 x18ba5f9 x1sbl2l xy9co9w x5r174s x7h3shv')
    n_messages = soup_messages.text if soup_messages else ''
    pinned = bool(soup.find('span', {'data-icon': 'pinned2'}))
    soup_muted = soup.find('div', {'aria-label': 'Muted chat'})
    muted = soup_muted.find('title').text if soup_muted else ''

    details = {
        'name': name,
        'time': chat_time,
        'text': text,
        'n_messages': n_messages,
        'pinned': pinned,
        'muted': muted
    }
    list.append(details)
    print(details)

driver.quit()