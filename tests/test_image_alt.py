import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from selenium.webdriver.common.by import By
from utils.browser import get_driver
from utils.excel_report import write_report
from config.settings import BASE_URL

class TestImageAltAttribute:
    def __init__(self):
        self.driver = get_driver()

    def run_image_alt_attribute_test(self):
        self.driver.get(BASE_URL)
        time.sleep(10) 

        test_case = "Image alt attribute test"
        try:
            images = self.driver.find_elements(By.TAG_NAME, 'img')
            missing_alt_count = 0

            # Count images missing alt attribute
            for img in images:
                alt_attribute = img.get_attribute('alt')
                if not alt_attribute:
                    missing_alt_count += 1

            if missing_alt_count > 0:
                result = "Fail"
                comments = f"{missing_alt_count} images missing `alt` attribute."
            else:
                result = "Pass"
                comments = "All images have `alt` attributes."

            results = [{"Page URL": BASE_URL, "Test Case": test_case, "Result": result, "Comments": comments}]
            
            write_report(test_case, BASE_URL, results)  # Pass results as a list of dictionaries
            print(f"Test {result.lower()}: {comments}")

        except Exception as e:
            results = [{"Page URL": BASE_URL, "Test Case": test_case, "Result": "Error", "Comments": str(e)}]
            write_report(test_case, BASE_URL, results)
            print(f"An error occurred: {e}")

    def close_driver(self):
        self.driver.quit()


if __name__ == "__main__":
    tester = TestImageAltAttribute()
    try:
        tester.run_image_alt_attribute_test()
    finally:
        tester.close_driver()
