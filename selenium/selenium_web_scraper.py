from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Search keyword variable
search_keyword = "EEG with AI"

service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)

driver.get("https://scholar.google.com/")

# Wait for the search input box and input the search keyword
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".gs_in_txt.gs_in_ac"))
)
input_element = driver.find_element(By.CSS_SELECTOR, ".gs_in_txt.gs_in_ac")
input_element.clear()
input_element.send_keys(search_keyword + Keys.ENTER)

# Wait for the search results to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.gs_ri"))
)

# Collect the 10 most relevant results (titles, links, and abstracts)
results = driver.find_elements(By.CSS_SELECTOR, "div.gs_ri")[:10]
for index, result in enumerate(results, start=1):
    title = result.find_element(By.CSS_SELECTOR, "h3.gs_rt").text
    link = result.find_element(By.CSS_SELECTOR, "h3.gs_rt a").get_attribute('href')
    # Attempt to find the abstract text; it might not always be present.
    try:
        abstract = result.find_element(By.CSS_SELECTOR, "div.gs_rs").text
    except:
        abstract = "Abstract not available."
    print(f"Result {index}: {title}\nLink: {link}\nAbstract: {abstract}\n")

time.sleep(5)  # Short pause to review output before exiting
driver.quit()
