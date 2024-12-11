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
        # Initialize the driver
        self.driver = get_driver()

    def run_currency_filter_test(self):
        self.driver.get(BASE_URL)
        time.sleep(2)  # Wait for the page to load completely

        test_case = "Currency filter test"
        results = []  # Store results for each currency
        headers = ["Currency", "Default Price", "Tile Prices", "Status"]

        try:
            # Wait for the currency dropdown to be present
            currency_dropdown = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "js-currency-sort-footer"))
            )

            # Scroll to the dropdown to ensure visibility
            self.driver.execute_script("arguments[0].scrollIntoView(true);", currency_dropdown)
            time.sleep(1)

            # Open the dropdown
            currency_dropdown.click()
            time.sleep(1)

            # Find all currency options
            currency_options = self.driver.find_elements(By.XPATH, "//div[@id='js-currency-sort-footer']//ul[@class='select-ul']//li")
            print(f"Currency options found: {len(currency_options)}")
            if not currency_options:
                raise Exception("No currency options found in the dropdown.")

            # Capture initial prices
            initial_default_price = self.driver.find_element(By.ID, "js-default-price").text.strip()
            print(f"Initial default price: {initial_default_price}")

            initial_tile_prices = [
                price.text.strip() for price in self.driver.find_elements(By.CLASS_NAME, "js-price-value")
            ]
            print(f"Initial tile prices: {initial_tile_prices}")

            # Iterate over each currency option and test
            for option in currency_options:
                currency_text = option.find_element(By.TAG_NAME, "p").text.strip()
                print(f"Testing currency: {currency_text}")

                try:
                    # Ensure the option is visible and clickable
                    WebDriverWait(self.driver, 10).until(EC.visibility_of(option))
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(option))

                    # Scroll into view and click on the currency option
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", option)
                    option.click()
                    print(f"Clicked on {currency_text}")
                except TimeoutException:
                    print(f"TimeoutException: Element {currency_text} not clickable.")
                    continue
                except StaleElementReferenceException:
                    print(f"StaleElementReferenceException: Retry clicking {currency_text}")
                    continue

                time.sleep(2)  # Wait for the page to update

                # Capture updated prices
                updated_default_price = self.driver.find_element(By.ID, "js-default-price").text.strip()
                print(f"Updated default price: {updated_default_price}")

                updated_tile_prices = [
                    price.text.strip() for price in self.driver.find_elements(By.CLASS_NAME, "js-price-value")
                ]
                print(f"Updated tile prices: {updated_tile_prices}")

                # If the currency is EUR, we skip price comparison because no change is expected
                if currency_text == "€ (EUR)":
                    status = "Pass"
                    print(f"Currency is EUR, no price change expected.")
                else:
                    # Compare prices for other currencies
                    if initial_default_price != updated_default_price:
                        print(f"Default price updated: {initial_default_price} → {updated_default_price}")
                        status = "Pass"
                    else:
                        print(f"Default price did not update.")
                        status = "Fail - No update"

                # Format the tile prices for Excel output as "From $124, From $130, ..."
                formatted_tile_prices = ', '.join([f"From {price}" for price in updated_tile_prices])

                # Add the result to the report
                results.append({
                    "Currency": currency_text,
                    "Default Price": updated_default_price,
                    "Tile Prices": formatted_tile_prices,
                    "Status": status
                })

                # Reopen the dropdown if necessary for the next selection
                currency_dropdown.click()
                time.sleep(1)

            # Write results to the report
            write_report(test_case, BASE_URL, results, headers)

        except Exception as e:
            # Log the full exception details
            write_report(test_case, BASE_URL, [{
                "Currency": "N/A",
                "Default Price": "N/A",
                "Tile Prices": "N/A",
                "Status": f"Fail - {traceback.format_exc()}"
            }], headers)
            print(f"Test failed: {traceback.format_exc()}")

        finally:
            print(f"Test completed. Results saved.")

    def close_driver(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
            print("Driver closed.")
        else:
            print("Driver not initialized.")


if __name__ == "__main__":
    tester = TestCurrencyFilter()
    try:
        tester.run_currency_filter_test()
    finally:
        tester.close_driver()