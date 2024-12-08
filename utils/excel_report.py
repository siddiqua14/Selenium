import os
import openpyxl

def write_report(test_case, result, comments, page_url):
    file_name = "data/test_results.xlsx"
    directory = os.path.dirname(file_name)

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.exists(file_name):
        workbook = openpyxl.load_workbook(file_name)
    else:
        workbook = openpyxl.Workbook()

    # Remove the existing sheet for this test if it exists
    if test_case in workbook.sheetnames:
        del workbook[test_case]

    # Create a new sheet for the test case
    sheet = workbook.create_sheet(title=test_case)
    sheet.append(["Page URL", "Test Case", "Result", "Comments"])
    sheet.append([page_url, test_case, result, comments])

    # Save the workbook
    workbook.save(file_name)
