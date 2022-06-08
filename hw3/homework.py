import pandas as pd
import pickle

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from prefect import flow, task, get_run_logger
from prefect.task_runners import SequentialTaskRunner

from datetime import datetime

def log_message(message_to_log):
    logger = get_run_logger()
    logger.info(message_to_log)

# @task
def read_data(path):
    df = pd.read_parquet(path)
    return df


# @task
def prepare_features(df, categorical, train=True):
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    mean_duration = df.duration.mean()
    if train:
        log_message(f"The mean duration of training is {mean_duration}")
        print(f"The mean duration of training is {mean_duration}")
    else:
        log_message(f"The mean duration of validation is {mean_duration}")
        print(f"The mean duration of validation is {mean_duration}")
    
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df


# @task
def get_paths(date=None):

    path_prefix = "./data/fhv_tripdata_"
    file_type = ".parquet"

    if date:
        date_conv = datetime.strptime(date, "%Y-%m-%d")
        curr_year = str(date_conv.year)
        curr_month = f"{(date_conv.month - 1):02d}"
        prev_month =  f"{(date_conv.month - 2):02d}"
    else:
        curr_year = str(datetime.now().year)
        curr_month = f"{(datetime.now().month - 1):02d}"
        prev_month =  f"{(datetime.now().month - 2):02d}"

    curr_path = path_prefix + curr_year + '-' + curr_month + file_type
    prev_path = path_prefix + curr_year + '-' + prev_month + file_type

    log_message(f"{prev_path}, {curr_path}")
    print(f"{prev_path}, {curr_path}")

    return prev_path, curr_path


@task
def train_model(df, categorical):

    train_dicts = df[categorical].to_dict(orient='records')
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts) 
    y_train = df.duration.values

    log_message(f"The shape of X_train is {X_train.shape}")
    log_message(f"The DictVectorizer has {len(dv.feature_names_)} features")

    print(f"The shape of X_train is {X_train.shape}")
    print(f"The DictVectorizer has {len(dv.feature_names_)} features")

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_train)
    mse = mean_squared_error(y_train, y_pred, squared=False)
    log_message(f"The MSE of training is: {mse}")
    print(f"The MSE of training is: {mse}")
    return lr, dv


@task
def run_model(df, categorical, dv, lr):
    val_dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(val_dicts) 
    y_pred = lr.predict(X_val)
    y_val = df.duration.values

    mse = mean_squared_error(y_val, y_pred, squared=False)
    log_message(f"The MSE of validation is: {mse}")
    print(f"The MSE of validation is: {mse}")
    return


@flow(task_runner=SequentialTaskRunner())
def main(date):

    categorical = ['PUlocationID', 'DOlocationID']

    train_path, val_path = get_paths(date)

    df_train = read_data(train_path)
    df_train_processed = prepare_features(df_train, categorical)

    df_val = read_data(val_path)
    df_val_processed = prepare_features(df_val, categorical, False)

    # train the model
    lr, dv = train_model(df_train_processed, categorical).result()

    with open(f"models/dv-{date}.b", "wb") as f_out:
            pickle.dump(dv, f_out)

    with open(f"models/model-{date}.bin", "wb") as f_out:
            pickle.dump(lr, f_out)

    run_model(df_val_processed, categorical, dv, lr)

# main(date="2021-08-15")

from prefect.deployments import DeploymentSpec
from prefect.orion.schemas.schedules import CronSchedule
from prefect.flow_runners import SubprocessFlowRunner

DeploymentSpec(
    name="model_training_hw3_cron",
    flow_location="/Users/aliakseikaravaichyk/git-repos/khv-mlops-zoomcamp/hw3/homework.py",
    schedule=CronSchedule(cron="0 9 15 * *"),
    flow_runner=SubprocessFlowRunner()
)