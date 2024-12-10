import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium.webdriver.common.by import By
from utils.browser import get_driver
from utils.excel_report import write_report
from config.settings import BASE_URL

class TestH1Tags:
    def __init__(self):
        self.driver = get_driver()

    def run_h1_tag_test(self):
        """
        Check for the existence of an H1 tag on the given page (BASE_URL).
        """
        self.driver.get(BASE_URL)
        time.sleep(2)  # Wait for the page to load completely

        test_case = "H1 tag existence test"
        try:
            # Check if an H1 tag exists
            self.driver.find_element(By.TAG_NAME, 'h1')
            # Create a result dictionary for the H1 tag test
            results = [{"Page URL": BASE_URL, "Test Case": test_case, "Result": "Pass", "Comments": "H1 tag found."}]
            write_report(test_case, BASE_URL, results)  # Pass results as a list of dictionaries
            print(f"Test passed: H1 tag exists on {BASE_URL}.")
        except:
            # If no H1 tag is found, record a failure
            results = [{"Page URL": BASE_URL, "Test Case": test_case, "Result": "Fail", "Comments": "H1 tag missing."}]
            write_report(test_case, BASE_URL, results)  # Pass results as a list of dictionaries
            print(f"Test failed: H1 tag missing on {BASE_URL}.")

    def close_driver(self):
        self.driver.quit()


if __name__ == "__main__":
    tester = TestH1Tags()
    
    try:
        tester.run_h1_tag_test()  # Correct method call
    finally:
        tester.close_driver()