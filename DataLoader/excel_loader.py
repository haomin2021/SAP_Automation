import pandas as pd

def load_excel(file_path):
    try:
        return pd.read_excel(file_path, header=None)
    except Exception as e:
        raise RuntimeError("Failed to load Excel file:\n" + str(e))
