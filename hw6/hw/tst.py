import batch
from datetime import datetime
import pandas as pd

options = {
        'client_kwargs': {
            'endpoint_url': "http://localhost:4566"
        }
    }


def read_data(filename):
    print(filename)
    df = pd.read_parquet(filename, storage_options=options)
    return df

df = read_data('s3://nyc-duration/out/2021-01.parquet')

print(df['predicted_duration'].sum())