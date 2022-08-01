import batch
from datetime import datetime
import pandas as pd
from pandas import Timestamp
from deepdiff import DeepDiff

def dt(hour, minute, second=0):
    return datetime(2021, 1, 1, hour, minute, second)

def test_df_preparartion():

    data = [
        (None, None, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2, 0), dt(1, 2, 50)),
        (1, 1, dt(1, 2, 0), dt(2, 2, 1)),        
    ]

    columns = ['PUlocationID', 'DOlocationID', 'pickup_datetime', 'dropOff_datetime']
    df = pd.DataFrame(data, columns=columns)

    categorical = ['PUlocationID', 'DOlocationID']
    df_act_res = batch.prepare_data(df=df, categorical_features=categorical)
    actual_result = df_act_res.to_dict(orient='records')

    expected_result = [
        {
            'PUlocationID': '-1',
            'DOlocationID': '-1',
            'pickup_datetime': Timestamp('2021-01-01 01:02:00'),
            'dropOff_datetime': Timestamp('2021-01-01 01:10:00'),
            'duration': 8.0
        },
        {
            'PUlocationID': '1',
            'DOlocationID': '1',
            'pickup_datetime': Timestamp('2021-01-01 01:02:00'),
            'dropOff_datetime': Timestamp('2021-01-01 01:10:00'),
            'duration': 8.0
        }
    ]

    diff = DeepDiff(actual_result, expected_result, significant_digits=1)
    print(f'diff={diff}')

    assert 'values_changed' not in diff
