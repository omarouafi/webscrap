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

driver.get('https://www.welcometothejungle.com/fr/jobs?page=1&refinementList%5Bprofession_name.fr.Tech%5D%5B%5D=Data%20Analysis&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDI')

time.sleep(5)
body = driver.find_element(By.TAG_NAME, 'body')

soup = BeautifulSoup(body.get_attribute('innerHTML'), 'html.parser')

list_jobs_container = soup.find_all('li', attrs={'data-testid': 'search-results-list-item-wrapper'})

with open('jobs.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Job Title', 'Company', 'Location'])

    for job in list_jobs_container:
        job_title = job.find('h4').text
        job_company = job.find('span', {'class': 'sc-ERObt'}).text
        job_location = job.find('p', {'class': 'wui-text'}).text

        writer.writerow([job_title, job_company, job_location])

driver.quit()
