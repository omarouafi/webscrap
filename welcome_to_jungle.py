import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import mysql.connector

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


def get_jobs(soup):
    list_jobs_container = soup.find_all('li', attrs={'data-testid': 'search-results-list-item-wrapper'})

    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="welcome_to_jungle"
    )

    cursor = db_connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            job_title VARCHAR(255),
            company VARCHAR(255),
            location VARCHAR(255)
        )
    """)

    for job in list_jobs_container:
        job_title = job.find('h4').text
        job_company = job.find('span', {'class': 'sc-ERObt'}).text
        job_location = job.find('p', {'class': 'wui-text'}).text

        sql = "INSERT INTO jobs (job_title, company, location) VALUES (%s, %s, %s)"
        val = (job_title, job_company, job_location)
        cursor.execute(sql, val)

    db_connection.commit()
    db_connection.close()


get_jobs(soup)
driver.quit()
