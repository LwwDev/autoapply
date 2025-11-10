import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#--- config
FIRST_NAME = "Liam"
LAST_NAME = "Wohlstedt"
EMAIL = "liam@wohlstedt.com"
PHONE = "+46706655011"
LINKEDIN = "https://www.linkedin.com/in/liamww/"
CV_PATH = r"C:\Users\lw\Documents\Liam\Liam Wohlstedt - Resume 2025.pdf"

SEARCH = ""
MAX_PAGES = 4








# ----------------- FUNCTIONS -----------------
def is_teamtailor(url):
    return "teamtailor.com/jobs" in url

def apply_teamtailor_job(driver, url):
    driver.get(url)
    time.sleep(2)  # wait for page to load

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "candidate[first_name]"))
        )
        driver.find_element(By.NAME, "candidate[first_name]").send_keys(FIRST_NAME)
        driver.find_element(By.NAME, "candidate[last_name]").send_keys(LAST_NAME)
        driver.find_element(By.NAME, "candidate[email]").send_keys(EMAIL)
        driver.find_element(By.NAME, "candidate[phone_number]").send_keys(PHONE)
        driver.find_element(By.NAME, "candidate[cv]").send_keys(CV_PATH)

        print(f"Filled application for {url}")
        time.sleep(1)

        # Optional: submit button
        # driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]").click()

    except Exception as e:
        print(f"Failed on {url}: {e}")

def scrape_linkedin_jobs(driver):
    job_urls = []

    for page in range(0, MAX_PAGES * 25, 25):  # LinkedIn shows 25 jobs per page
        url = f"{LINKEDIN_BASE_URL}&start={page}"
        driver.get(url)
        time.sleep(3)  # wait for page to load

        try:
            jobs = driver.find_elements(By.XPATH, "//a[contains(@href,'linkedin.com/jobs/view')]")
            for job in jobs:
                href = job.get_attribute("href")
                if href not in job_urls:
                    job_urls.append(href)
        except Exception as e:
            print(f"Failed to scrape page {page//25 + 1}: {e}")

    return job_urls

# ----------------- MAIN -----------------
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
driver.maximize_window()

print("Scraping LinkedIn job URLs...")
linkedin_jobs = scrape_linkedin_jobs(driver)
print(f"Found {len(linkedin_jobs)} LinkedIn jobs.")

for job_url in linkedin_jobs:
    if is_teamtailor(job_url):
        print(f"Applying to Teamtailor job: {job_url}")
        apply_teamtailor_job(driver, job_url)
    else:
        print(f"Skipping non-Teamtailor job: {job_url}")

driver.quit()
