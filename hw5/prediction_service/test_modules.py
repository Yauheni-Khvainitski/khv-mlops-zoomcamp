import os
import pickle
import requests

from pymongo import MongoClient

from flask import Flask, request, jsonify


MODEL_FILE = os.getenv('MODEL_FILE', 'lin_reg.bin')
MONGODB_ADDRESS = os.getenv('MONGODB_ADDRESS', 'mongodb://127.0.0.1:27017')
EVIDENTLY_SERVICE_ADDRESS = os.getenv('EVIDENTLY_SERVICE_', 'http://127.0.0.1:8085')


with open(MODEL_FILE, 'rb') as f_in:
    dv, model = pickle.load(f_in)

# app = Flask('duration-prediction')
# mongo_client = MongoClient(MONGODB_ADDRESS)
# db = mongo_client.get_database('prediction_service')
# collection = db.get_collection('data')


# def save_to_db(record, prediction):
#     rec = record.copy()
#     rec['prediction'] = prediction

#     collection.insert_one(rec)


# def send_to_evidently_service(record, prediction):
#     rec = record.copy()
#     rec['prediction'] = prediction

#     requests.post(f"{EVIDENTLY_SERVICE_ADDRESS}/iterate/taxi", json=[rec])


# @app.route('/predict', methods=['POST'])
# def predict():
ride = {
    'lpep_pickup_datetime': '2021-01-01 00:15:56',
    'PULocationID': 43,
    'DOLocationID': 151,
    'passenger_count': 1.0,
    'trip_distance': 1.01
}

ride['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])

print(ride)

X = dv.transform([ride])
y_pred = model.predict(X)

result = {
    'duration': float(y_pred),
}

print(result)

#     save_to_db(record, float(y_pred))
#     send_to_evidently_service(record, float(y_pred))
#     return jsonify(result)


# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0', port=9696)
