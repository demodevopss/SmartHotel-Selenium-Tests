import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = webdriver.chrome.service.Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()

def test_title(driver):
    # Get the application URL from an environment variable
    app_url = os.environ.get('APP_URL')
    assert app_url, "APP_URL environment variable is not set"
    driver.get(app_url)
    assert "SmartHotel360" in driver.title

def test_switch_tab(driver):
    app_url = os.environ.get('APP_URL')
    assert app_url, "APP_URL environment variable is not set"
    driver.get(app_url)
    repositories_tab = driver.find_element(By.ID, "repositories")
    repositories_tab.click()
    repositories_content = driver.find_element(By.ID, "Repositories")
    assert repositories_content.is_displayed()
