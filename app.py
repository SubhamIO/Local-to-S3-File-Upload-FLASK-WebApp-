# Importing essential libraries
from flask import Flask, render_template, request
import pickle
import numpy as np
import os
import sys
print("===PATH===", os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/Desktop/flask_s3_uploads/")
import numpy as np
import pandas as pd
from numpy import array
from math import sqrt
from flask import jsonify, request
from flask_restful import Resource
import boto3
from botocore.exceptions import ClientError
import logging
from flask import current_app
import json
import pickle
import random, string
import csv
import datetime
import flask

#from s3_uploader import *
from helpers import *
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/index')
def index():
    return flask.render_template('index.html')



@app.route('/predict', methods=['POST'])
def predict():


    if request.files['trained_data_set'] and 'user_id' in request.form :
        random_str = x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        millisec_str = str(datetime.datetime.now().timestamp()).replace(".", "")
        date_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        final_random_str = random_str +"_"+millisec_str+"_"+ date_str
        #jdata = jsonify({"success":False, "data": ""})

        #Read data from user
        trained_data_set_csv = request.files['trained_data_set']
        test_data_set_csv = request.files['test_data_set']
        print(trained_data_set_csv,test_data_set_csv)


        user_id = request.form['user_id']
        print(user_id)

        #upload to local system
        tr_filename_trained, tr_file_extension_trained = os.path.splitext(trained_data_set_csv.filename)
        print(tr_filename_trained,tr_file_extension_trained)
        tr_final_file_name = final_random_str+tr_file_extension_trained
        #/Users/subham/Desktop/flask_s3_uploads/upload-aiml-automation/trained-data-set/rcjQRrOfVM4SvtHA_1603090047596287_20201019121727.csv
        trained_data_set_csv.save(os.path.join(UPLOAD_FOLDER+"/"+TRAINED_DATA_SET_FOLDER, tr_final_file_name))

        te_filename_trained, te_file_extension_trained = os.path.splitext(test_data_set_csv.filename)
        print(te_filename_trained,te_file_extension_trained)
        te_final_file_name = final_random_str+te_file_extension_trained
        #/Users/subham/Desktop/flask_s3_uploads/upload-aiml-automation/trained-data-set/rcjQRrOfVM4SvtHA_1603090047596287_20201019121727.csv
        test_data_set_csv.save(os.path.join(UPLOAD_FOLDER+"/"+TEST_DATA_SET_FOLDER, te_final_file_name))

        jdata_tr = upload_files_to_s3(user_id,tr_final_file_name,TRAINED_DATA_SET_FOLDER,'train')
        jdata_te = upload_files_to_s3(user_id,te_final_file_name,TEST_DATA_SET_FOLDER,'test')
        if (jdata_tr == 'True' and jdata_te=='True'):
            result = 'Files are Uploaded to S3'
        else:
            result = 'Files upload incomplete - Internal Server Error!'

    else :
            result = 'Invalid File'

    return render_template("index.html",prediction_text=result)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
