from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import BROWSER_SETTINGS

def get_driver():
    options = Options()
    # Configure browser window size
    options.add_argument(f"--window-size={BROWSER_SETTINGS['window_size']}")
    
    # Ensure headless is disabled
    if not BROWSER_SETTINGS.get("headless", False):
        options.add_argument("--disable-headless")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver
