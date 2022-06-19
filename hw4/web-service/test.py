import requests
# import predict    # for local testing w/o flask app

ride = {
    "PULocationID": 10,
    "DOLocationID": 50,
    "trip_distance": 40
}

# test without a running flask server
# features = predict.prepare_features(ride)
# preds = predict.predict(features)
# print(preds)

url = 'http://52.201.248.234:9696/predict' # 'http://127.0.0.1:9696/predict'
response = requests.post(url, json=ride)
print(response.json())
