import pandas as pd
from .config import DATA_FILE


def load_raw(file_path=None, sheet_name=None):
    path = file_path or DATA_FILE
    xl = pd.ExcelFile(path)
    data_sheet = sheet_name or (
        "data" if "data" in xl.sheet_names else xl.sheet_names[-1]
    )
    return pd.read_excel(path, sheet_name=data_sheet, header=0)
