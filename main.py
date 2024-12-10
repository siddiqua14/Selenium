from tests.test_currency_filter import TestCurrencyFilter
from tests.test_h1_tags import TestH1Tags
from tests.test_html import TestHTMLTagSequence 
from tests.test_image_alt import TestImageAltAttribute
from tests.test_scrape import TestScrapeData
from tests.test_urls import TestURLStatusCode

def run_all_tests():
    # Initialize the test classes
    currency_test = TestCurrencyFilter()
    h1_tag_test = TestH1Tags()
    html_test = TestHTMLTagSequence()   # Assuming the test class is created for test_html.py
    image_alt_test = TestImageAltAttribute()  # Assuming the test class is created for test_image_alt.py
    scrape_test = TestScrapeData()
    urls_test = TestURLStatusCode()  # Assuming the test class is created for test_urls.py

    # Run each test
    try:
        print("Running Currency Filter Test...")
        currency_test.run_currency_filter_test()

        print("Running H1 Tag Test...")
        h1_tag_test.run_h1_tag_test()

        print("Running HTML Test...")
        html_test.run_html_tag_sequence_test()  # Assuming you have implemented run_html_test()

        print("Running Image Alt Test...")
        image_alt_test.run_image_alt_attribute_test()  # Assuming you have implemented run_image_alt_test()

        print("Running Scrape Test...")
        scrape_test.run_scrape_test()

        print("Running URL Test...")
        urls_test.run_url_status_code_test()  # Assuming you have implemented run_urls_test()

    except Exception as e:
        print(f"Test execution failed: {e}")
    finally:
        # Ensure proper cleanup after tests
        currency_test.close_driver()
        h1_tag_test.close_driver()
        html_test.close_driver()
        image_alt_test.close_driver()
        scrape_test.close_driver()
        urls_test.close_driver()

if __name__ == "__main__":
    run_all_tests()
