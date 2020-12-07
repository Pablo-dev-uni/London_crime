from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import time

# coding=utf-8
  
import sys
import os
import glob
import re
import numpy as np

from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer





app = Flask(__name__)


def model_predict(img_path):
    ENDPOINT = "https://drclass-prediction.cognitiveservices.azure.com/"
    prediction_key = "5412cdf1a9bb4c8d8df7f42a24c28cbf"
    prediction_resource_id = '9147ebd0-f315-4c8b-9e76-1ecf5a92ffe5'

    prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
    predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

# Now there is a trained endpoint that can be used to make a prediction
    prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
    predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

# Now there is a trained endpoint that can be used to make a prediction
    prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
    predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

    project_id= '97dbe87d-c6e3-4f0f-8103-f71b5bd281ed'
    publish_iteration_name = 'Iteration1'
    with open( img_path, "rb") as image_contents:
        results = predictor.classify_image(
            project_id, publish_iteration_name, image_contents.read())

    # Display the results.
    for prediction in results.predictions:
        return prediction.tag_name+ ' '+ str(prediction.probability)
   


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        result = model_predict(file_path)
        
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)