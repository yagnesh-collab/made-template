import os
import zipfile
import urllib.request
import pandas as pd
import sqlite3
import shutil

def download_and_extract_data(download_url: str, zip_path: str, extracted_folder: str) -> None:
    urllib.request.urlretrieve(download_url, zip_path)

    # Unzip the file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extracted_folder)

def reshape_data(data_path: str, data_filename: str) -> pd.DataFrame:
    try:
        # Read the CSV data into a DataFrame with specific options
        df = pd.read_csv(os.path.join(data_path, data_filename),
                         sep=';',
                         index_col=False,
                         usecols=['Geraet', 'Hersteller', 'Model', 'Monat', 'Temperatur in °C (DWD)', 'Batterietemperatur in °C', 'Geraet aktiv'],
                         decimal=',')

        # Drop columns to the right of "Geraet aktiv"
        df = df.loc[:, :"Geraet aktiv"]

        # Change the name of the columns
        df = df.rename(columns={"Temperatur in °C (DWD)": "Temperatur", "Batterietemperatur in °C": "Batterietemperatur"})

        return df
    except pd.errors.ParserError as e:
        print(f"Error parsing the CSV file: {e}")
        return pd.DataFrame()

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    # Convert temperatures to Fahrenheit
    df["Temperatur"] = (df["Temperatur"] * 9/5) + 32
    df["Batterietemperatur"] = (df["Batterietemperatur"] * 9/5) + 32

    return df

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df[(df["Geraet"] > 0) & (df["Monat"].between(1, 12))]
    return df

def write_to_sqlite(df: pd.DataFrame, db_file: str, table_name: str) -> None:
    conn = sqlite3.connect(db_file)
    df.to_sql(table_name, conn, index=False, if_exists="replace")
    print('Stored in te database')
    conn.close()

def data_pipeline(download_url, zip_file_path, extracted_folder, data_file_path, db_file, table_name):
    # Download and extract data
    download_and_extract_data(download_url, zip_file_path, extracted_folder)

    # Reshape data: read CSV with specific options
    df = reshape_data(extracted_folder, "data.csv")

    # Transform data: convert temperature
    df = transform_data(df)

    # Validate data: “Geraet” to be an id over 0, and month between 1 to 12
    df = validate_data(df)

    # Write data into SQLite database
    write_to_sqlite(df, db_file, table_name)

    # Remove downloaded ZIP file and extracted folder
    os.remove(zip_file_path)
    shutil.rmtree(extracted_folder)  # Use shutil.rmtree to remove non-empty directories

    print("All operations completed successfully")

download_url = "https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip"
zip_file_path = "mowesta-dataset.zip"
extracted_folder = "mowesta-dataset"
data_file_path = os.path.join(extracted_folder, "data.csv")
db_file = "temperatures.sqlite"
table_name = "temperatures"

data_pipeline(download_url, zip_file_path, extracted_folder, data_file_path, db_file, table_name)