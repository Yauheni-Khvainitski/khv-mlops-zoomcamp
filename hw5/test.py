import requests

url = 'http://127.0.0.1:9696/predict' # 'http://3.88.13.33:9696/predict'

ride = {
    'lpep_pickup_datetime': '2021-01-01 00:15:56',
    'PULocationID': 43,
    'DOLocationID': 151,
    'passenger_count': 1.0,
    'trip_distance': 1.01
}

response = requests.post(url, json=ride).json()
print(response)
