import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium.webdriver.common.by import By
from utils.browser import get_driver
from utils.report import write_report  
from config.settings import BASE_URL

class TestScrapeData:
    def __init__(self):
        self.driver = get_driver()

    def run_scrape_test(self):
        self.driver.get(BASE_URL)
        time.sleep(10)

        test_case = "Scrape Data Test"
        try:
            script_data = self.driver.execute_script("return window.ScriptData;")
            site_url = script_data.get('config', {}).get('SiteUrl', '')
            site_name = script_data.get('config', {}).get('SiteName', '')
            campaign_id = script_data.get('pageData', {}).get('CampaignId', '')
            country_code = script_data.get('userInfo', {}).get('CountryCode', '')
            ip = script_data.get('userInfo', {}).get('IP', '')

            browser = self.driver.capabilities['browserName']
            result = "Pass"  # This is the result status
            result_message = (
                f"Successfully scraped data: "
                f"SiteName: {site_name}, CampaignID: {campaign_id}, CountryCode: {country_code}, IP: {ip}"
            )

            # Log the result to Excel using the write_report function
            write_report(site_url, site_name, campaign_id, browser, country_code, ip, result)

            print(f"Test passed: Data scraped successfully from {BASE_URL}.")
        except Exception as e:
            result = "Fail"  
            result_message = f"Error while scraping data: {str(e)}"
            write_report('', '', '', '', '', '', result)  # Empty values for failed test

            print(f"Test failed: {result_message}")

    def close_driver(self):
        self.driver.quit()


if __name__ == "__main__":
    tester = TestScrapeData()
    
    try:
        tester.run_scrape_test()
    finally:
        tester.close_driver()
