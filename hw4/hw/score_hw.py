#!/usr/bin/env python
# coding: utf-8

import sys
import pickle
import pandas as pd
from datetime import datetime

from sklearn.feature_extraction import DictVectorizer

from dateutil.relativedelta import relativedelta


with open('model.bin', 'rb') as f_in:
    dv, lr = pickle.load(f_in)

categorical = ['PUlocationID', 'DOlocationID']


def get_year_month(run_date):
    prev_month = run_date - relativedelta(months=1)
    year = prev_month.year
    month = prev_month.month

    return year, month


def get_paths(run_date, taxi_type, run_id):

    year, month = get_year_month(run_date)

    input_file = f's3://nyc-tlc/trip data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f's3://nyc-taxi-duration-prediction/output/taxi_type={taxi_type}/year={year:04d}/month={month:02d}/{run_id}.parquet'

    return input_file, output_file


def read_dataframe(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


def prepare_dictionaries(df: pd.DataFrame):
    dicts = df[categorical].to_dict(orient='records')
    return dicts


def save_results(df, run_date, y_pred, output_file):

    year, month = get_year_month(run_date)

    df_result = pd.DataFrame()
    df_result['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    df_result['predicted_duration'] = y_pred
    
    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
        )


taxi_type = sys.argv[1]  # fhv
year = int(sys.argv[2])  # 2021
month = int(sys.argv[3]) # 3
run_id = sys.argv[4]
run_date=datetime(year=year, month=month, day=1)

input_file, output_file = get_paths(run_date, taxi_type, run_id=run_id)

print(f'reading dataset {input_file} ...')
df = read_dataframe(input_file)

print('converting dataframe to dictionaries...')
dicts = prepare_dictionaries(df)

print('getting feature matrix...')
X_val = dv.transform(dicts)

print('getting predictions...')
y_pred = lr.predict(X_val)

print(f'saving results to {output_file} ...')
df_result = save_results(
    df=df,
    run_date=run_date,
    y_pred=y_pred,
    output_file=output_file
)

print(y_pred.mean())

# q1 16.191691679979066
# q2 19711507 ~ 19 M
# q3 jupyter nbconvert --to script starter.ipynb
# q4 sha256:08ef968f6b72033c16c479c966bf37ccd49b06ea91b765e1cc27afefe723920b
# q5 16.298821614015107
# q6 9.967573179784523