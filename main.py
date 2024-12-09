import time
from tests.test_h1_tags import TestH1Tags  # Import your test classes
from tests.test_urls import TestURLStatusCode  # Another test for URL status, for example

def run_tests():
    # Define the base URL to be used for testing
    base_url = "https://www.alojamiento.io/"
    
    # Initialize the test classes you want to run
    tester_h1 = TestH1Tags()
    tester_url = TestURLStatusCode()

    try:
        # Running the tests
        print("Running H1 Tags Test...")
        tester_h1.check_links_and_run_tests(base_url)  # Call the method from TestH1Tags class
        
        print("Running URL Status Test...")
        tester_url.run_url_status_code_test()  # Call the method from TestURLStatusCode class
        
    finally:
        # Ensure that the browser is closed after the tests are done
        tester_h1.close_driver()
        tester_url.close_driver()

if __name__ == "__main__":
    run_tests()
