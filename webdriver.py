import time
import os
import pandas as pd

from RPA.Browser.Selenium import Selenium
from selenium.webdriver.common.by import By

import settings


class WebDriver(Selenium):
    browser = Selenium()

    # Open browser, set download path and get url
    def open_web_browser(self):
        self.browser.set_download_directory(
            directory=settings.DOWNLOAD_DIR,
            download_pdf=True
        )

        self.browser.open_available_browser()

    # Click the button to open
    def click(self, locator_value):
        self.browser.click_element_when_visible(
            locator=locator_value,
        )

    # Search for agencies and amounts and add to list
    def search_for_agencies_and_amount(self, agencie_locator_value, amount_locator_value):

        agencies_list = self.browser.find_elements(
            locator=agencie_locator_value,
        )

        amount_list = self.browser.find_elements(
            locator=amount_locator_value,
        )

        agencies_and_amount_dict = {k.text: v.text for (k, v) in zip(agencies_list, amount_list)}

        df = pd.DataFrame(
            data=agencies_and_amount_dict.items(),
            columns=['Agencies', 'Amount']
        )

        return df

    # Get the agencie url for scraping table
    def get_agencie_url(self, agencie_name):
        agencie_url = self, self.browser.find_element(
            locator=f'xpath://div[contains(@class,"wrapper")]//a[contains(.,"{agencie_name}")]',
        )

        return agencie_url

    # Set full table view
    def set_table_view(self, value_locator, key):
        self.browser.press_key(
            locator=value_locator,
            key=key,
        )

    # Get the Individual Investments table
    def get_table(self, column_names_locator, rows_locator):
        column_names = self.browser.find_elements(
            locator=column_names_locator,
        )

        rows_parents = self.browser.find_elements(
            locator=rows_locator,
        )

        rows = [row.find_elements(By.XPATH, './td') for row in rows_parents]

        df = pd.DataFrame(
            data=[[x.text for x in row] for row in rows],
            columns=[x.text for x in column_names],
        )

        return df

    # Get the UII links from table
    def get_UII_links(self, link_locator):
        link_elemens_list = self.browser.find_elements(
            locator=link_locator,
        )

        link_list = [link.get_attribute('href') for link in link_elemens_list]

        return link_list

    # Download pdf files
    def download_pdf(self, link_list, pdf_locator):
        for link in link_list:
            self.browser.go_to(
                url=link
            )
            self.browser.wait_until_element_is_visible(
                locator=pdf_locator,
            )

            try:
                self.browser.click_element(
                    locator=f'{pdf_locator}/a',
                )
                while self.browser.does_page_contain(
                    text='Generating PDF...'):
                    time.sleep(1)
                else:
                    continue
            except:
                continue

        while any([filename.endswith(".crdownload") for filename in
                   os.listdir(settings.DOWNLOAD_DIR)]):
            time.sleep(1)
