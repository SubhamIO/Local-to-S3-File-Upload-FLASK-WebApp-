# Importing essential libraries
from flask import Flask, render_template, request
import pickle
import numpy as np
import os
import sys
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
UPLOAD_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/Desktop/flask_s3_uploads/"+"upload-aiml-automation"
TRAINED_DATA_SET_FOLDER = 'trained-data-set'
TEST_DATA_SET_FOLDER = 'test-data-set'
PREDICTION_OUTPUT_FOLDER = 'prediction-output'
S3_BUCKET_NAME = 'mlbankproject27091995'
ALLOWED_EXTENSIONS = {'csv'}
s3_client = boto3.client(
    's3',
    aws_access_key_id="#",
    aws_secret_access_key="#",
)


def upload_files_to_s3(user_id,final_file_name,DATA_SET_FOLDER,purpose_file):


    random_str = x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    millisec_str = str(datetime.datetime.now().timestamp()).replace(".", "")
    date_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    final_random_str = random_str +"_"+millisec_str+"_"+ date_str
    jdata = 'False'



    try:
        #inside AWS S3 bucket follow the same folder structure to get results
        if purpose_file == 'train':
            s3_bucket_key_name = user_id+"/data/train/train_data_set.csv"
        else:
            s3_bucket_key_name = user_id+"/data/test/test_data_set.csv"
        s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=s3_bucket_key_name)
        s3_client.put_object(
            Body=open(UPLOAD_FOLDER+"/"+DATA_SET_FOLDER+"/"+final_file_name, encoding='utf_8').read(),
            Bucket=S3_BUCKET_NAME,
            Key=s3_bucket_key_name)
        if os.path.exists(UPLOAD_FOLDER+"/"+DATA_SET_FOLDER+"/"+final_file_name):
            os.remove(UPLOAD_FOLDER+"/"+DATA_SET_FOLDER+"/"+final_file_name)
        jdata = 'True'

    except ClientError as e:
        logging.error(e)
        jdata = 'False'

    return jdata
