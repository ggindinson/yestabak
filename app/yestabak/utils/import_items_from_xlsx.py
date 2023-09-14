from openpyxl.cell import Cell
from openpyxl import load_workbook
from yestabak.api_wrapper.api_classes import ImportedItem
import pprint


def import_items_from_xlsx(file_path: str):
    wb_sheets = load_workbook(filename=file_path)

    data = {}
    for wb_sheet in wb_sheets:
        data[wb_sheet.title] = [
            ImportedItem(name=str(item[0]), price=float(item[1])) for item in wb_sheet.values
        ]

    return data
