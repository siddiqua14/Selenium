# Vacation Rental Home Page Automation Testing

## Description
This project automates the testing of a vacation rental details page to validate essential elements and functionality. Built with **Python**, **Selenium**, and **Pandas**, the automation scripts focus on:

- Testing SEO-related elements.
- Validating webpage functionality.
- Generating comprehensive Excel reports for analysis.

### Primary Goals:
- **Compliance with SEO standards.**
- **Smooth user experience** through functional currency filters and working URLs.
- **Accurate data scraping** for key elements.

## Features
1. **H1 Tag Existence Test**  
   Ensures the presence of an H1 tag on the page.

2. **HTML Tag Sequence Test**  
   Validates the proper order of heading tags (H1 to H6).

3. **Image Alt Attribute Test**  
   Checks that all images have appropriate alt attributes.

4. **URL Status Code Test**  
   Ensures all URLs are functional (e.g., no 404 errors).

5. **Currency Filter Test**  
   Verifies the currency filter updates the property prices as expected.

6. **Data Scraping Test**  
   Extracts critical metadata (e.g., site URL, campaign ID, country code) and logs it.

7. **Comprehensive Reporting**  
   All test results and data scraping outputs are stored in Excel for clarity and accessibility.
## Prerequisites

Ensure the following requirements are met before running the automation scripts:

1. **Python**  
   - Version: 3.8 or later.  
   - [Download Python](https://www.python.org/downloads/)

2. **Browser**  
   - Google Chrome or Mozilla Firefox must be installed.  
   - [Download Google Chrome](https://www.google.com/chrome/)  
   - [Download Firefox](https://www.mozilla.org/firefox/)

3. **WebDriver Manager**
    - The project uses the `webdriver_manager` library to automatically download and manage the appropriate WebDriver version, so no manual installation is required.  


## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/siddiqua14/Selenium.git
   cd Selenium
   ```
2. Set up a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the Tests

### Run all tests:
To run all the automated tests, use the following command:

```bash
python main.py
```
### Run individual tests:
To run a specific test, such as the currency filter test, use:
```bash
python tests/test_currency_filter.py
```

## Configuration

All configurations are managed in `config/settings.py`:

- **BASE_URL**: URL of the page to test (currently set to the vacation rental page).

- **BROWSER_SETTINGS**:
  - **headless**: Whether to run the browser in headless mode (True/False).
  - **window_size**: Sets the browser window size.

- **EXCEL_REPORT_PATH**: Path for the generated Excel reports.


markdown
Copy code
## Output Reports

### Test Results (`test_results.xlsx`)

The test results are stored in an Excel file, with the following columns:

| **Page URL**                                   | **Test Case**             | **Pass/Fail** | **Comments**                                   |
|------------------------------------------------|---------------------------|---------------|-----------------------------------------------|
| https://www.alojamiento.io/property/charming-apartment-in-awesome-sevilla-with-ac-wifi/HA-61511677097 | H1 Tag Existence Test      | Pass          | H1 tag found                                  |
| https://www.alojamiento.io/property/charming-apartment-in-awesome-sevilla-with-ac-wifi/HA-61511677097 | HTML tag sequence test       | Fail          | Missing tags: h5, h6         |
| https://www.alojamiento.io/property/charming-apartment-in-awesome-sevilla-with-ac-wifi/HA-61511677097 | Image Alt Attribute Test   | Pass          | All images have alt attributes                |
| https://www.alojamiento.io/property/charming-apartment-in-awesome-sevilla-with-ac-wifi/HA-61511677097 | Currency Filter Test       | Pass           | Property tiles updated correctly with all currencies: <br> Pass: $ (USD), Pass: $ (CAD), Pass: € (EUR), Pass: £ (GBP), Pass: $ (AUD), Pass: $ (SGD), Pass: ﷼ (AED), Pass: ৳ (BDT) |
---

## Scraped Data (`scraped_data_report.xlsx`)


The scraped data is stored in an Excel file with the following format:

| **Site URL**                 | **Site Name** | **Campaign ID** | **Browser** | **Country Code** | **IP Address**     | **Result** |
|------------------------------|---------------|-----------------|-------------|------------------|--------------------|------------|
| https://www.alojamiento.io    | alo           | ALOJAMIENTO     | Chrome      | BD               | 182.160.106.203    | Pass      |

---

## Tests Overview

1. **H1 Tag Test (`test_h1_tags.py`)**  
   Checks for the presence of an H1 tag.  
   Fails if no H1 tag is found.

2. **HTML Tag Sequence Test (`test_html.py`)**  
   Validates the sequence of heading tags (H1 to H6) for proper structure.

3. **Image Alt Attribute Test (`test_image_alt.py`)**  
   Ensures all images have an alt attribute to meet SEO standards.

4. **URL Status Code Test (`test_urls.py`)**  
   Checks all URLs for valid HTTP status codes (e.g., not 404).

5. **Currency Filter Test (`test_currency_filter.py`)**  
   Tests if the currency filter updates property prices across tiles.  
   Logs any mismatched currency in the Excel report.

6. **Data Scraping Test (`test_scrape.py`)**  
   Extracts metadata such as Site URL, Campaign ID, Country Code, and IP Address.  
   Logs the data in a separate Excel file.
## Dependencies

This project requires the following Python packages:

- **selenium**: For browser automation.
- **pandas**: For Excel report generation.
- **openpyxl**: For writing to Excel files.
- **requests**: For handling HTTP requests.
- **webdriver-manager**: For automatically managing WebDriver installations.

To install all dependencies, run:

```bash
pip install selenium pandas openpyxl requests webdriver-manager
```

## Reusability of Code

The project is designed with reusability and scalability in mind:

- **Modular Design**: Each test is isolated in its own file, making it easy to add or modify tests without affecting others.
  
- **Centralized Utilities**: Common functions like browser setup and Excel reporting are placed in the `utils` module, ensuring reusability across tests.

- **Configuration File**: All key settings (e.g., base URL, browser options) are defined in `config/settings.py`, enabling quick updates without code changes.

- **Extensibility**: The modular structure allows for new tests to be added with minimal effort.
