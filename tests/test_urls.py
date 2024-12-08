import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from selenium.webdriver.common.by import By
from utils.browser import get_driver
from utils.excel_report import write_report
from config.settings import BASE_URL

class TestURLStatusCode:
    def __init__(self):
        self.driver = get_driver()

    def run_url_status_code_test(self):
        """
        Test to validate the status codes of all links on the page.
        If any link returns a 404 status code, the test fails.
        """
        self.driver.get(BASE_URL)
        time.sleep(10)  # Wait for the page to load completely

        test_case = "URL status code test"
        try:
            links = self.driver.find_elements(By.TAG_NAME, 'a')  # Find all anchor tags
            broken_links_count = 0
            comments = []

            for link in links:
                href = link.get_attribute('href')
                if href:  # Ensure href attribute is not None or empty
                    try:
                        response = requests.head(href, timeout=5)  # Perform a HEAD request
                        if response.status_code == 404:  # Check for broken link
                            broken_links_count += 1
                            comments.append(f"Broken link: {href}")
                    except requests.RequestException as e:
                        # Handle request errors
                        broken_links_count += 1
                        comments.append(f"Error accessing {href}: {str(e)}")

            if broken_links_count > 0:
                result = "Fail"
                comments_str = f"{broken_links_count} broken links found.\n" + "\n".join(comments)
            else:
                result = "Pass"
                comments_str = "No broken links found."

            # Write the result to the Excel report
            write_report(test_case, result, comments_str, BASE_URL)
            print(f"Test {result.lower()}: {comments_str}")

        except Exception as e:
            # Log unexpected errors in the report
            write_report(test_case, "Error", str(e), BASE_URL)
            print(f"An error occurred: {e}")

    def close_driver(self):
        self.driver.quit()


if __name__ == "__main__":
    tester = TestURLStatusCode()
    try:
        tester.run_url_status_code_test()
    finally:
        tester.close_driver()
