import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy

def load_csv_data(url: str) -> pd.DataFrame:
    try:
        dataframe = pd.read_csv(url, sep=';', decimal=',')
        return dataframe
    except pd.errors.EmptyDataError:
        print('Error: Empty file.')
        return pd.DataFrame()
    except Exception as error:
        print(f'Error: {error}')
        return None

if __name__ == '__main__':
    # URL of CSV file
    data = 'https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV'
    
    # Read dataframe from the csv file
    dataframe = load_csv_data(data)
    
    # Filtering dataframe according to the requirement
    dataframe = (
        dataframe
        .drop(columns=['Status'])
        .dropna()
        .query('Verkehr in ["FV", "RV", "nur DPN"]')
        .query('-90 < Laenge < 90')
        .query('-90 < Breite < 90')
        .query('IFOPT.str.match("^..:[0-9]+:[0-9]+(:[0-9]+)?$")', engine='python')
    )

    engine = create_engine('sqlite:///trainstops.sqlite')
    
    try:
        dataframe.to_sql('trainstops', engine, if_exists='replace', index=False, dtype={
            "EVA_NR": sqlalchemy.BIGINT,
            "DS100": sqlalchemy.TEXT,
            "IFOPT": sqlalchemy.TEXT,
            "NAME": sqlalchemy.TEXT,
            "Verkehr": sqlalchemy.TEXT,
            "Laenge": sqlalchemy.FLOAT,
            "Breite": sqlalchemy.FLOAT,
            "Betreiber_Name": sqlalchemy.TEXT,
            "Betreiber_Nr": sqlalchemy.BIGINT
        })
        print("Table created successfully.")
    except Exception as e:
        print(f"Error: {e}")