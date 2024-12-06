import time
import openpyxl
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

# Function to create or load the Excel workbook and sheet
def create_excel_report(test_case):
    try:
        workbook = openpyxl.load_workbook("test_results.xlsx")
    except FileNotFoundError:
        workbook = openpyxl.Workbook()

    # Create the "currency_filtering" sheet or load it if it already exists
    if "currency_filtering" not in workbook.sheetnames:
        sheet = workbook.create_sheet(title="currency_filtering")
        # Write headers for the sheet
        sheet.append(["Test Case", "Currency", "Result", "Comments"])
    else:
        sheet = workbook["currency_filtering"]
    
    return workbook, sheet

# Function to write results into the Excel file
def write_report(test_case, currency, result, comments):
    workbook, sheet = create_excel_report(test_case)
    sheet.append([test_case, currency, result, comments])
    workbook.save("test_results.xlsx")

# Initialize WebDriver
options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to perform currency filtering (click dropdown and select currency)
def perform_currency_filtering(currency):
    try:
        # Locate the currency dropdown and click it
        currency_filter = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "currency-selector"))  # Adjust this to the correct ID
        )
        currency_filter.click()

        # Locate and click the currency option based on the given currency
        currency_option = driver.find_element(By.XPATH, f"//option[text()='{currency}']")
        currency_option.click()
        time.sleep(3)  # Wait for the page to reload with the new currency

        return True
    except Exception as e:
        return False

# Function to check property tiles' currency after filtering
def check_property_tiles_currency(currency):
    # Check that the currency displayed in the property tiles matches the selected currency
    property_tiles = driver.find_elements(By.CLASS_NAME, "property-tile")  # Adjust this to the correct class name

    for tile in property_tiles:
        try:
            currency_text = tile.find_element(By.CLASS_NAME, "currency").text  # Adjust the class name accordingly
            if currency_text != currency:
                write_report("Currency Filtering Test", currency, "Fail", f"Currency mismatch in property tile: {currency_text}")
                return False
        except Exception as e:
            write_report("Currency Filtering Test", currency, "Fail", "Error retrieving currency from property tile.")
            return False
    
    # If all property tiles show the correct currency
    write_report("Currency Filtering Test", currency, "Pass", f"Currency successfully changed to {currency}")
    return True

# Function to collect all unique URLs from the page
def collect_unique_urls():
    driver.get("https://www.alojamiento.io/")
    time.sleep(2)  # Wait for the page to load

    # Collect all links on the page
    links = driver.find_elements(By.TAG_NAME, "a")
    unique_urls = set([link.get_attribute('href') for link in links if link.get_attribute('href')])  # Ensure uniqueness

    return unique_urls

# Main function to run the test on all unique URLs
def run_currency_filtering_tests():
    unique_urls = collect_unique_urls()  # Collect all unique URLs from the main page

    # List of currencies to test (example: USD, EUR, GBP)
    currencies_to_test = ["USD", "EUR", "GBP"]

    for currency in currencies_to_test:
        # Step 1: Perform currency filtering
        if perform_currency_filtering(currency):
            # Step 2: Check all unique URLs for currency change
            for url in unique_urls:
                driver.get(url)  # Visit each unique URL
                time.sleep(3)  # Wait for the page to load completely
                check_property_tiles_currency(currency)
        else:
            write_report("Currency Filtering Test", currency, "Fail", f"Failed to change currency to {currency}")

# Run the currency filtering tests
run_currency_filtering_tests()

# Close the browser
try:
    driver.quit()
except WebDriverException as e:
    print(f"Error closing the browser: {e}")
