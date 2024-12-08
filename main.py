from tests.test_h1_tags import TestH1Tags

if __name__ == "__main__":
    base_url = "https://www.alojamiento.io/"
    tester = TestH1Tags()
    
    try:
        tester.check_links_and_run_tests(base_url)
    finally:
        tester.close_driver()
