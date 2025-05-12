import os
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

# 1) Load credentials from .env
load_dotenv()
HS_SCHOOL = os.getenv("school")
HS_EMAIL    = os.getenv("email")
HS_PASSWORD = os.getenv("password")

# 2) Handshake login URL
LOGIN_URL = "https://app.joinhandshake.com/login"

def get_driver(headless: bool = False) -> webdriver.Chrome:
    """
    Creates and returns a Chrome WebDriver using webdriver-manager.
    """
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver

def login(driver: webdriver.Chrome, timeout: int = 15) -> None:
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver, timeout)

    # —— Step 1: open the school dropdown ——
    trigger = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR, 
        ".select2-choice"       # the box you click to open the dropdown
    )))
    trigger.click()

    # —— Step 2: type your school name ——
    school_input = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR,
        "input.select2-input"   # the search box that appears
    )))
    school_input.clear()
    school_input.send_keys(HS_SCHOOL)

    # —— Step 3: choose the first result ——
    first_option = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR,
        "li.select2-results__option, li.select2-result-selectable"
        # different versions of Select2 use one of these classes
    )))
    first_option.click()
    try: 
        sso_btn = wait.until(EC.element_to_be_clickable((By.ID, "sso-name")))
        sso_btn.click()
        print("→ Clicked SSO login button")
    except:
        print("→ No SSO button detected, continuing...")

    # Step 2: Wait for the ASU credential form
    # Inspect the actual ASU form to confirm these IDs—common ones are 'username' & 'password'
    username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_input = driver.find_element(By.ID, "password")

    # Step 3: Fill in your ASU (school) credentials
    username_input.clear()
    username_input.send_keys(HS_EMAIL)
    password_input.clear()
    password_input.send_keys(HS_PASSWORD)
    print("→ Entered ASU credentials")

    # Step 4: Submit the ASU form
    # The submit button may be <button type="submit"> or <input type="submit" ...>
    submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']|//input[@type='submit']")
    submit_btn.click()
    print("→ Submitted ASU login form")

    long_wait = WebDriverWait(driver, 60)  # wait up to 60 seconds
    long_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/jobs']")))

    print("✅ Logged in to Handshake")
    