import os
from openpyxl import Workbook

def write_report(site_url, campaign_id, site_name, browser, country_code, ip, test_case, result):
    report_file = os.path.join(os.path.dirname(__file__), "..", "data", "scrape_report.xlsx")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(report_file), exist_ok=True)

    try:
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Scrape Report"
        sheet.append(["Site URL", "Campaign ID", "Site Name", "Browser", "Country Code", "IP", "Test Case", "Result"])
        sheet.append([site_url, campaign_id, site_name, browser, country_code, ip, test_case, result])
        workbook.save(report_file)
        print(f"Report saved at: {report_file}")
    except Exception as e:
        print(f"Failed to write report: {e}")
