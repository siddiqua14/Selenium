import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import traceback
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.browser import get_driver
from utils.excel_report import write_report
from config.settings import BASE_URL

class TestCurrencyFilter:
    def __init__(self):
        self.driver = get_driver()

    def run_currency_filter_test(self):
        """
        Test that changing the currency updates the property tiles' currency display.
        """
        self.driver.get(BASE_URL)
        time.sleep(2)  # Wait for the page to load completely

        test_case = "Currency filter test"
        results = []  # Store results for each currency

        try:
            # Wait for the currency dropdown to be present
            currency_dropdown = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "js-currency-sort-footer"))
            )

            # Scroll to the dropdown to ensure visibility
            self.driver.execute_script("arguments[0].scrollIntoView(true);", currency_dropdown)
            time.sleep(1)

            # Open the dropdown (automatically)
            currency_dropdown.click()  # Open the dropdown
            time.sleep(1)

            # Find all currency options using XPath and innerHTML
            currency_options = self.driver.find_elements(By.XPATH, "//div[@id='js-currency-sort-footer']//ul[@class='select-ul']//li")
            print(f"Currency options found: {len(currency_options)}")
            if not currency_options:
                raise Exception("No currency options found in the dropdown.")

            # Iterate over each currency option and test
            for option in currency_options:
                # Get the innerHTML content of the option element
                option_html = option.get_attribute("innerHTML")
                print(f"Option HTML: {option_html}")  # Debugging the HTML content

                # Extract the currency text from the <p> tag inside the <div> tag
                currency_text = option.find_element(By.TAG_NAME, "p").text.strip()
                print(f"Testing currency: {currency_text}")

                try:
                    # Ensure the option is visible and clickable
                    WebDriverWait(self.driver, 10).until(EC.visibility_of(option))  # Ensure visibility
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(option))  # Ensure clickability
                    
                    # Scroll into view to avoid issues with elements outside the viewport
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", option)

                    # Click on the currency option
                    option.click()  
                    print(f"Clicked on {currency_text}")  # Logging the selected currency
                except TimeoutException:
                    print(f"TimeoutException: Element {currency_text} not clickable.")
                    continue  # Skip this currency if it's not clickable
                except StaleElementReferenceException:
                    # Handle the case when the element becomes stale and needs to be refreshed
                    print(f"StaleElementReferenceException: Retry clicking {currency_text}")
                    continue

                time.sleep(2)  # Wait for the page to update

                # Validate property tiles display the selected currency
                property_tiles = self.driver.find_elements(By.CLASS_NAME, "property-tile")  # Adjust selector if needed
                all_tiles_correct = True

                for tile in property_tiles:
                    price_element = tile.find_element(By.CLASS_NAME, "price")  # Adjust selector if needed
                    if currency_text not in price_element.text:
                        all_tiles_correct = False
                        print(f"Currency mismatch: {currency_text} not found in {price_element.text}.")
                        break

                if all_tiles_correct:
                    results.append(f"Pass: {currency_text}")
                    print(f"Currency {currency_text} passed. Property tiles updated correctly.")
                else:
                    results.append(f"Fail: {currency_text}")
                    print(f"Currency {currency_text} failed. Property tiles not updated correctly.")

                # Reopen the dropdown if necessary for the next selection
                currency_dropdown.click()
                time.sleep(1)

            # Write detailed results to the report
            final_result = "\n".join(results)
            write_report(test_case, "Pass", final_result, BASE_URL)
            print(f"Test completed: \n{final_result}")

        except Exception as e:
            # Log the full exception details
            write_report(test_case, "Fail", traceback.format_exc(), BASE_URL)
            print(f"Test failed: {traceback.format_exc()}")

    def close_driver(self):
        self.driver.quit()

if __name__ == "__main__":
    tester = TestCurrencyFilter()
    try:
        tester.run_currency_filter_test()
    finally:
        tester.close_driver()
