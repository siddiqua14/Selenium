import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium.webdriver.common.by import By
from utils.browser import get_driver
from utils.report import write_report  # Assuming this function writes to Excel
from config.settings import BASE_URL

class TestScrapeData:
    def __init__(self):
        self.driver = get_driver()

    def run_scrape_test(self):
        """
        Scrape data from the page (BASE_URL) and check for the required elements.
        """
        self.driver.get(BASE_URL)
        time.sleep(2)  # Wait for the page to load completely

        test_case = "Scrape Data Test"
        try:
            # Extract the script data from the page
            script_data = self.driver.execute_script("return window.ScriptData;")
            #print("Script Data:", script_data)  # Debug: Log the entire script data

            # Extract required data from the script data
            site_url = script_data.get('config', {}).get('SiteUrl', '')
            site_name = script_data.get('config', {}).get('SiteName', '')
            campaign_id = script_data.get('pageData', {}).get('CampaignId', '')
            country_code = script_data.get('userInfo', {}).get('CountryCode', '')
            ip = script_data.get('userInfo', {}).get('IP', '')

            # Prepare the data for the report
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
            # If any error occurs, record a failure
            result = "Fail"  # Test failed
            result_message = f"Error while scraping data: {str(e)}"
            write_report('', '', '', '', '', '', result)  # Empty values for failed test

            print(f"Test failed: {result_message}")

    def close_driver(self):
        self.driver.quit()


if __name__ == "__main__":
    tester = TestScrapeData()
    
    try:
        tester.run_scrape_test()  # Run the scrape test
    finally:
        tester.close_driver()
