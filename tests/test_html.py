import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium.webdriver.common.by import By
from utils.browser import get_driver
from utils.excel_report import write_report
from config.settings import BASE_URL

class TestHTMLTagSequence:
    def __init__(self):
        self.driver = get_driver()

    def run_html_tag_sequence_test(self):
        """
        Check for the existence and sequence of HTML tags (H1 to H6) on the given page (BASE_URL).
        """
        self.driver.get(BASE_URL)
        time.sleep(2)  # Wait for the page to load completely

        test_case = "HTML tag sequence test"
        tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        missing_tags = []
        broken_sequence = False

        try:
            last_tag_index = -1
            for tag in tags:
                try:
                    self.driver.find_element(By.TAG_NAME, tag)
                    tag_index = tags.index(tag)
                    if tag_index < last_tag_index:
                        broken_sequence = True
                    last_tag_index = tag_index
                except:
                    missing_tags.append(tag)

            # Preparing the result as a dictionary list
            if missing_tags or broken_sequence:
                result = "Fail"
                comments = f"Missing tags: {', '.join(missing_tags)}"
                if broken_sequence:
                    comments += " | Sequence broken."
            else:
                result = "Pass"
                comments = "All tags from H1 to H6 found in sequence."

            results = [{"Page URL": BASE_URL, "Test Case": test_case, "Result": result, "Comments": comments}]
            
            # Write the result to the Excel report
            write_report(test_case, BASE_URL, results)  # Passing the results as a list of dictionaries
            print(f"Test result for {BASE_URL}: {result} - {comments}")

        except Exception as e:
            # Log unexpected errors in the report
            results = [{"Page URL": BASE_URL, "Test Case": test_case, "Result": "Error", "Comments": str(e)}]
            write_report(test_case, BASE_URL, results)
            print(f"Error running test: {e}")

    def close_driver(self):
        self.driver.quit()


if __name__ == "__main__":
    tester = TestHTMLTagSequence()
    try:
        tester.run_html_tag_sequence_test()
    finally:
        tester.close_driver()
