from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

 # Set up options for the Chrome WebDriver
options = webdriver.ChromeOptions()


    # Start a Selenium WebDriver with options
driver = webdriver.Chrome(options=options)


url = 'https://www.linkedin.com/'
driver.get(url)


# Find the username and password input fields and login button
username_input = driver.find_element('name', 'session_key')
password_input = driver.find_element('name', 'session_password')


# Input your LinkedIn credentials
username_input.send_keys('youremail@gmail.com')
password_input.send_keys('yourpassword')

# Find and wait for the login button to be clickable
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
)

# Click the login button
login_button.click()

time.sleep(10)

# Wait for the login process to complete
try:
    # Wait until the search bar appears, indicating a successful login
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@role="combobox"]'))
    )
except Exception as e:
    print(f"Login failed: {e}")
    driver.quit()

# Navigate to the Jobs section
job_titles = []
company_names = []
apply_links = []

for i in range(0, 1000, 25):
    driver.get(f"https://www.linkedin.com/jobs/search/?f_E=2&keywords=Data%20Engineer&location=India&start={i}")
    time.sleep(10)

    # Get the HTML content of the current page
    page_html = driver.page_source
    
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(page_html, 'html.parser')

    company_name = soup.find_all('span', class_='job-card-container__primary-description')
    job_title = soup.find_all('a', class_='disabled ember-view job-card-container__link job-card-list__title')
    for name in company_name:
        n = name.text.strip()
        company_names.append(n)
    for title in job_title:
        t = title.text.strip()
        job_titles.append(t)
    for link in job_title:
        l = link['href']
        apply_links.append(f"https://www.linkedin.com/{l}")


print(len(company_names), len(job_titles), len(apply_links))

if len(company_names) == len(job_titles):
    df = pd.DataFrame({'company_names': company_names, 'job_titles': job_titles, 'apply_links': apply_links})
    df.to_csv("Data_Engineer_jobs.csv", index=False, header=True)
else:
    print("lengths doesn't match")


# Close the browser window
driver.quit()



