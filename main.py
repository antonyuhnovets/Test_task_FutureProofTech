import time
import pandas as pd

from RPA.Browser.Selenium import Selenium
from selenium.webdriver.common.by import By


browser_lib = Selenium()

AGENCIE_TO_GET_DATA_FROM = 'Department of Agriculture'

# Open browser, set download path and get url
def open_the_website(url):
    browser_lib.set_download_directory(
        directory="D:/Work/Python/projects/Test_task_TheFutureProofTechnology/output",
        download_pdf=True
    )

    browser_lib.open_available_browser(
        url=url,
    )


# Click the button to open
# TODO: wait untill page loaded
def click(locator_value):
    browser_lib.click_element_when_visible(
        locator=locator_value,
    )


# Search for agencies and amounts and add to list
def search_for_agencies_and_amount(container_locator, agencie_locator_value, amount_locator_value):
    browser_lib.wait_until_element_is_visible(
        locator=container_locator
    )

    agencies_list = browser_lib.find_elements(
        locator=agencie_locator_value,
    )

    amount_list = browser_lib.find_elements(
        locator=amount_locator_value,
    )

    agencies_and_amount_dict = {k.text: v.text for (k,v) in zip(agencies_list, amount_list)}

    df = pd.DataFrame(
        data=agencies_and_amount_dict.items(),
        columns=['Agencies', 'Amount']
    )

    return df


# Get the agencie url for scraping table
def get_agencie_url(agencie_name):
    agencie_url = browser_lib.find_element(
        locator=f'xpath://div[contains(@class,"wrapper")]//a[contains(.,"{agencie_name}")]',
    )

    return agencie_url


# Set full table view
# TODO: wait untill table loads
def set_table_view(value_locator, key):
    browser_lib.press_key(
        locator=value_locator,
        key=key,
    )


# Get the Individual Investments table
def get_table(column_names_locator, rows_locator):
    column_names = browser_lib.find_elements(
        locator=column_names_locator,
    )

    rows_parents = browser_lib.find_elements(
        locator=rows_locator,
    )

    rows = [row.find_elements(By.XPATH, './td') for row in rows_parents]

    df = pd.DataFrame(
        data=[[x.text for x in row] for row in rows],
        columns=[x.text for x in column_names],
    )

    return df


# Get the UII links from table
# TODO: if element contain href
def get_UII_links(link_locator):
    link_elemens_list = browser_lib.find_elements(
        locator=link_locator,
    )

    link_list = [link.get_attribute('href') for link in link_elemens_list]

    return link_list


# Download pdf files
# TODO: wait until page loads, wait until download complete
def download_pdf(link_list):
    for link in link_list:
        time.sleep(2)

        browser_lib.go_to(
            url=link,
        )

        time.sleep(2)

        browser_lib.click_element_when_visible(
            locator='//*[@id="business-case-pdf"]/a',
        )

        time.sleep(3)


# Define a main() function that calls the other functions in order:
def main():
    try:
        open_the_website(
            url='https://itdashboard.gov/',
        )

        click(
            locator_value='//*[@id="node-23"]/div/div/div/div/div/div/div/a',
        )
        #TODO: wait untill page loaded
        time.sleep(15)

        agencies_amount_table = search_for_agencies_and_amount(
            container_locator='//*[@id="agency-tiles-container"]',
            agencie_locator_value='xpath://div[contains(@class,"wrapper")]//div[contains(@class, "col-sm-12")]//span[1]',
            amount_locator_value='xpath://div[contains(@class,"wrapper")]//div[contains(@class, "col-sm-12")]//span[2]',
        )

        agencie_url = get_agencie_url(
            agencie_name=AGENCIE_TO_GET_DATA_FROM,
        )

        browser_lib.go_to(
            url=agencie_url.get_attribute('href'),
        )
        #TODO: wait untill page loads
        time.sleep(15)

        set_table_view(
            value_locator='//*[@id="investments-table-object_length"]/label/select',
            key='All',
        )
        #TODO: wait untill table loads
        time.sleep(20)

        agencie_table = get_table(
            column_names_locator='//*[@id="investments-table-object_wrapper"]/div[3]/div[1]/div/table/thead/tr[2]/th',
            rows_locator='//*[@id="investments-table-object"]/tbody/tr',
        )

        pdf_links = get_UII_links(
            link_locator='xpath://*[@id="investments-table-object"]/tbody/tr/td[1]/a',
        )

        time.sleep(2)

        download_pdf(
            link_list=pdf_links,
        )

        with pd.ExcelWriter(
                path='./output/data_output.xlsx',
        ) as write:
            agencies_amount_table.to_excel(write, sheet_name='Agencies')
            agencie_table.to_excel(write, sheet_name=f'{AGENCIE_TO_GET_DATA_FROM}')

    finally:
        browser_lib.close_all_browsers()


# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()

