import os

from flask import Flask, request, jsonify
import mlflow

os.environ["AWS_PROFILE"] = "admin-pers"

RUN_ID = '22a623478ff84c878a59da6101e891da'
# MLFLOW_TRACKING_SERVER_HOST = '52.201.248.234'
# mlflow.set_tracking_uri(f"http://{MLFLOW_TRACKING_SERVER_HOST}:5000")

logged_model = f's3://mlflow-artifacts-remote-test/2/{RUN_ID}/artifacts/models' # f'runs:/{RUN_ID}/models'
model = mlflow.pyfunc.load_model(logged_model)

def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features


def predict(features):
    preds = model.predict(features)
    return float(preds[0])


app = Flask('duration-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()

    features = prepare_features(ride)
    pred = predict(features)

    result = {
        "duration": pred,
        "model_version": RUN_ID
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)