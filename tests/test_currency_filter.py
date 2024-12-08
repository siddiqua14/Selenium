
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from selenium.common.exceptions import TimeoutException
import traceback
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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

            # Open the dropdown
            ActionChains(self.driver).move_to_element(currency_dropdown).click().perform()
            time.sleep(1)

            # Find all currency options
            currency_options = self.driver.find_elements(By.CSS_SELECTOR, "#js-currency-sort-footer .select-ul li")
            print(f"Currency options found: {len(currency_options)}")
            if not currency_options:
                raise Exception("No currency options found in the dropdown.")

            # Iterate over each currency option and test
            for option in currency_options:
                currency_code = option.get_attribute("data-currency-country")
                print(f"Testing currency: {currency_code}")

                try:
                    # Ensure visibility and clickability
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", option)
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(option))
                    option.click()  # Select the currency
                except TimeoutException:
                    print(f"Element {currency_code} not clickable, forcing with JavaScript.")
                    self.driver.execute_script("arguments[0].click();", option)

                time.sleep(2)  # Wait for the page to update

                # Validate property tiles display the selected currency
                property_tiles = self.driver.find_elements(By.CLASS_NAME, "property-tile")  # Adjust selector if needed
                all_tiles_correct = True

                for tile in property_tiles:
                    price_element = tile.find_element(By.CLASS_NAME, "price")  # Adjust selector if needed
                    if currency_code not in price_element.text:
                        all_tiles_correct = False
                        print(f"Currency mismatch: {currency_code} not found in {price_element.text}.")
                        break

                if all_tiles_correct:
                    results.append(f"Pass: {currency_code}")
                    print(f"Currency {currency_code} passed.")
                else:
                    results.append(f"Fail: {currency_code}")
                    print(f"Currency {currency_code} failed.")

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
