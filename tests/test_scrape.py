# tests/test_scrape.py
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.settings import BASE_URL
from utils.report import write_report
from utils.browser import get_driver
import traceback

class ScrapeTester:
    def __init__(self):
        self.driver = get_driver()
        
    def scrape_and_record_data(self):
        try:
            # Navigate to the base URL
            self.driver.get(BASE_URL)
            
            # Scrape dynamic data from the web page
            site_name = self.driver.title  # Get the site name from the page title
            browser = self.driver.capabilities['browserName']  # Get the browser name

            # Extracting data dynamically from the page
            # Example: Assuming the data is embedded in a script tag or visible in HTML
            country_code = self.driver.execute_script("""
                return document.querySelector('meta[name="country-code"]')?.getAttribute('content') 
                || 'Unknown';
            """)  # Replace with actual scraping logic for country code

            ip = self.driver.execute_script("""
                return document.querySelector('meta[name="ip-address"]')?.getAttribute('content') 
                || 'Unknown';
            """)  # Replace with actual logic or elements containing the IP

            campaign_id = self.driver.execute_script("""
                return document.querySelector('script[data-campaign-id]')?.getAttribute('data-campaign-id') 
                || 'Unknown';
            """)  # Replace with logic to scrape the campaign ID

            # Write the data to an Excel file
            write_report(BASE_URL, campaign_id, site_name, browser, country_code, ip, "Scrape data test case", "Pass")

        except Exception as e:
            # Write to report in case of failure
            error_message = f"Fail: {traceback.format_exc()}"
            write_report(BASE_URL, "N/A", "N/A", "N/A", "N/A", "N/A", "Scrape data test case", error_message)

        finally:
            self.driver.quit()


if __name__ == "__main__":
    tester = ScrapeTester()
    tester.scrape_and_record_data()
