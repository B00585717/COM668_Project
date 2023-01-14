import datetime
import re
from datetime import timedelta
from random import randint

import bcrypt
from functools import wraps
import jwt
import pyodbc
from decouple import config
from flask import Flask, request, jsonify, make_response, json
from pymongo import MongoClient

from flask_cors import CORS

app = Flask(__name__)
app.secret_key = config('SK')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
CORS(app)

server = 'b00585717server.database.windows.net'
database = 'b00585717db'
username = config('UN', default='')
password = config('PW', default='')
driver = '{ODBC Driver 18 for SQL Server}'

conn = pyodbc.connect(
    'DRIVER=' + driver + ';SERVER=tcp:' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

cursor = conn.cursor()


if __name__ == "__main__":
    app.run(debug=True)
