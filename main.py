import time
import pandas as pd

import settings

from webdriver import WebDriver


# Website class
class ItDashboard(WebDriver):

    def get_agencies_names_and_amounts(self):
        self.browser.go_to(
            url='https://itdashboard.gov/',
        )

        self.click(
            locator_value='//*[@id="node-23"]/div/div/div/div/div/div/div/a',
        )

        while not self.browser.is_element_visible(locator='//*[@id="agency-tiles-widget"]/div'):
            time.sleep(1)

        agencies_amount_table = self.search_for_agencies_and_amount(
            agencie_locator_value='xpath://div[contains(@class,"wrapper")]//div[contains(@class, '
                                  '"col-sm-12")]//span[1]',
            amount_locator_value='xpath://div[contains(@class,"wrapper")]//div[contains(@class, '
                                 '"col-sm-12")]//span[2]',
        )

        return agencies_amount_table

    def get_table_data(self):
        agencie_url = self.get_agencie_url(
            agencie_name=settings.AGENCIE_TO_GET_DATA_FROM,
        )

        self.browser.go_to(
            url=agencie_url[1].get_attribute('href'),
        )

        while not self.browser.is_element_visible(locator='//*[@id="investments-table-object"]'):
            time.sleep(1)

        self.set_table_view(
            value_locator='//*[@id="investments-table-object_length"]/label/select',
            key='All',
        )

        while self.browser.is_element_visible(locator='//*[@id="investments-table-object_paginate'
                                                      '"]/span/a[2]'):
            time.sleep(1)

        agencie_table = self.get_table(
            column_names_locator='//*[@id="investments-table-object_wrapper"]/div[3]/div['
                                 '1]/div/table/thead/tr[2]/th',
            rows_locator='//*[@id="investments-table-object"]/tbody/tr',
        )

        return agencie_table

    def get_pdf_files(self):
        pdf_links = self.get_UII_links(
            link_locator='xpath://*[@id="investments-table-object"]/tbody/tr/td[1]/a',
        )

        time.sleep(2)

        self.download_pdf(
            link_list=pdf_links,
            pdf_locator='//*[@id="business-case-pdf"]',
        )

    def write_to_excel(self):
        agencies_amounts = self.get_agencies_names_and_amounts()
        agencie_table = self.get_table_data()

        with pd.ExcelWriter(
                path='./output/data_output.xlsx',
        ) as write:
            agencies_amounts.to_excel(write, sheet_name='Agencies')
            agencie_table.to_excel(write, sheet_name=f'{settings.AGENCIE_TO_GET_DATA_FROM}')


def main():
    obj = ItDashboard()
    obj.open_web_browser()
    obj.write_to_excel()
    obj.get_pdf_files()
    obj.close_all_browsers()


# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()



