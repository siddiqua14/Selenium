from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# Initialize WebDriver
options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open vacation rental website
driver.get("https://www.alojamiento.io/")

# Get all anchor tags and extract hrefs
links = driver.find_elements(By.TAG_NAME, "a")
unique_urls = set()

for link in links:
    href = link.get_attribute("href")
    if href:  # Ensure the href attribute exists
        unique_urls.add(href)

# Print the count of unique URLs
print(f"Total links found: {len(links)}")
print(f"Unique URLs: {len(unique_urls)}")

# Close the driver
driver.quit()
