import zipfile
import shutil
import pandas as pd
import sqlite3
from kaggle.api.kaggle_api_extended import KaggleApi

def extract_zip(old_name: str, new_name: str):
    shutil.move(old_name, new_name)
    with zipfile.ZipFile(new_name, 'r') as zip_ref:
        zip_ref.extractall('co2_emission')

def read_and_preprocess(file_path, nan_fill_value=0, encoding='latin-1'):
    data = pd.read_csv(file_path, encoding=encoding)
    data.fillna(nan_fill_value, inplace=True)
    return data

def save_to_csv_and_sql(data, csv_path, sql_path, table_name):
    data.to_csv(csv_path, index=False)
    conn = sqlite3.connect(sql_path)
    data.to_sql(table_name, conn, index=False, if_exists='replace')
    conn.close()

if __name__ == "__main__":
    api = KaggleApi()
    api.authenticate()

    # download the datasets
    api.dataset_download_file('moazzimalibhatti/co2-emission-by-countries-year-wise-17502022/data','CO2 emission by countries.csv')
    api.dataset_download_file('amirhoseinmousavian/renewable-energy-share/data','share-electricity-renewables.csv')
    extract_zip('CO2%20emission%20by%20countries.csv.zip', 'co2_emission.zip')

    # read the both datasets
    co2_data = read_and_preprocess('co2_emission/CO2 emission by countries.csv')

    # Read and preprocess Renewable Energy dataset
    renewables_data = read_and_preprocess('share-electricity-renewables.csv', nan_fill_value=0)
    renewables_data = renewables_data.rename(columns={'Entity': 'Country'})

    # Save datasets to CSV and SQLite
    save_to_csv_and_sql(co2_data, 'data/co2_emission.csv', 'data/co2_emission.db', 'co2_emission_data')
    save_to_csv_and_sql(renewables_data, 'data/renewables_data.csv', 'data/renewables_data.db', 'renewables_data')