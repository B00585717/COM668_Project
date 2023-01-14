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

@app.route("/api/v1.0/parties", methods=["GET"])
def show_all_parties():
    data_to_return = []
    query = "SELECT * FROM Party"
    cursor.execute(query)
    for row in cursor.fetchall():
        item_dict = {"Party ID": row[0], "Party Name": row[1]}
        data_to_return.append(item_dict)
    return make_response(jsonify(data_to_return), 200)


@app.route("/api/v1.0/parties/<id>", methods=["GET"])
def show_one_party(id):
    data_to_return = []
    query = "SELECT * FROM Party WHERE party_id = ?"
    cursor.execute(query, (id,))
    for row in cursor.fetchall():
        item_dict = {"Party ID": row[0], "Party Name": row[1]}
        data_to_return.append(item_dict)
    return make_response(jsonify(data_to_return), 200)


def edit_party():
    return 0


def delete_party():
    return 0


def add_candidate():
    return 0


@app.route("/api/v1.0/candidates", methods=["GET"])
def show_all_candidates():
    data_to_return = []
    query = "SELECT * FROM Candidate"
    cursor.execute(query)
    for row in cursor.fetchall():
        item_dict = {"Candidate ID": row[0], "Candidate First Name": row[1], "Candidate Surname": row[2]}
        data_to_return.append(item_dict)
    return make_response(jsonify(data_to_return), 200)


@app.route("/api/v1.0/candidates/<id>", methods=["GET"])
def show_one_candidate(id):
    data_to_return = []
    query = "SELECT * FROM Candidate WHERE candidate_id = ?"
    cursor.execute(query, id)
    for row in cursor.fetchall():
        item_dict = {"Candidate ID": row[0], "Candidate First Name": row[1], "Candidate Surname": row[2]}
        data_to_return.append(item_dict)
    return make_response(jsonify(data_to_return), 200)


if __name__ == "__main__":
    app.run(debug=True)
