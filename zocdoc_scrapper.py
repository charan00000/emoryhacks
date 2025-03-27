# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
import time
import undetected_chromedriver as uc

options = uc.ChromeOptions()
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = uc.Chrome(options=options)
with driver:
    driver.get("https://www.zocdoc.com")


