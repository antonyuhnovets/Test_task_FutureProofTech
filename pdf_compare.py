import os

from RPA.PDF import PDF
import pandas as pd
import openpyxl

import settings

pdf = PDF()

pdf_dict = dict()
excel_dict = dict()

# Get the data from files and add to dicts
for file_name in os.listdir(f'{settings.DOWNLOAD_DIR}'):
    # Get PDF files data
    if file_name.endswith('.pdf'):
        text = pdf.get_text_from_pdf(
            source_path=f'{settings.DOWNLOAD_DIR}/{file_name}',
            pages=1
        )
        element = text[1].split('Section B:')[0].split('. ')[-2:]
        pdf_dict[element[1].split(': ')[1]] = element[0].split(': ')[1][:-1]
    # Get Excel files data
    elif file_name.endswith('.xlsx'):
        excel_data = pd.read_excel(
            f'{settings.DOWNLOAD_DIR}/{file_name}',
            engine='openpyxl',
            sheet_name=f'{settings.AGENCIE_TO_GET_DATA_FROM}',
            usecols=['UII', 'Investment Title'],
        )
        excel_dict = excel_data.set_index('UII').T.to_dict('index')['Investment Title']

# Print out elements by id
for id in pdf_dict.keys():
    print(f'{id} in PDF: {pdf_dict[id]}, in Excel: {excel_dict[id]}')
