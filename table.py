import openpyxl
import pandas as pd
import json
from main import _cities_list


def save_to_table():
    """
    1. Read file
    2. Add columns with city names
    3. Read line
    4. Search price in cities by code

    :return:
    """
    wb = openpyxl.load_workbook('file.xlsx')
    sheet = wb['TDSheet']

    cities = _cities_list()[:50]
    for i, city in enumerate(cities):
        sheet.cell(row=1, column=i + 5).value = city[1]
    for col in range(1, sheet.max_column+1):
        sheet.column_dimensions[openpyxl.utils.get_column_letter(col)].auto_size = True
        sheet.cell(row=1, column=col)._style = sheet.cell(row=1, column=4)._style
    # add filters
    sheet.auto_filter.ref = sheet.dimensions

    for row in range(2, sheet.max_row + 1):
        articul = sheet.cell(row=row, column=1).value
        if articul is None:
            continue
        for i, city in enumerate(cities):
            with open(f'data/{city[0]}.json') as f:
                data = json.load(f)
                for item in data:
                    if item['code'] == articul:
                        sheet.cell(row=row, column=i + 5).value = item['price']
                        break

    wb.save('out_50_cities.xlsx')


if __name__ == '__main__':
    save_to_table()
