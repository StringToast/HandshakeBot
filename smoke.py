from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

print("🛠️  smoke.py is running!")

# 1) Create a Service using the downloaded driver
service = Service(ChromeDriverManager().install())

# 2) (Optional) You can add Chrome options here
options = webdriver.ChromeOptions()
# options.add_argument("--headless")   # run without opening a window

print("→ launching Chrome…")
driver = webdriver.Chrome(service=service, options=options)

print("→ navigating to example.com…")
driver.get("https://example.com")

print("→ page title:", driver.title)

time.sleep(3)
driver.quit()
print("✅ Done")