import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv

options = Options()
options.add_argument("--disable-extensions")
options.add_argument("--ignore-certificate-errors")

driver_path = ChromeDriverManager().install()
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://www.leboncoin.fr/f/voitures/u_car_brand--AUDI?locations=Nanterre_92000__48.88822_2.19428_4069_5000')

time.sleep(5)
body = driver.find_element(By.TAG_NAME, 'body')

soup = BeautifulSoup(body.get_attribute('innerHTML'), 'html.parser')
div = soup.find('div', {'data-test-id': 'adcard-big-picture'})
print(div)
driver.quit()
