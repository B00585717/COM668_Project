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

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.COM668_MongoDB

blacklist = db.Blacklist

email_regex = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'


@app.route("/api/v1.0/register", methods=["POST"])
def register():
    if "first_name" in request.form \
            and "last_name" in request.form \
            and "password" in request.form \
            and "email" in request.form:
        fn = request.form["first_name"]
        ln = request.form["last_name"]
        gid = gov_id_generator(8)
        pw = request.form["password"]
        c_id = 1
        email = request.form["email"]

        cursor.execute('SELECT * FROM Voter WHERE email = ?', (email,))
        user = cursor.fetchone()
        if user:
            return make_response("User already exists!", 403)

        elif not re.match(email_regex, email):
            return make_response("Invalid email address", 404)

        elif not fn or not ln or not pw or not email:
            return make_response("Please complete form", 404)

        elif len(pw) < 8:
            return make_response("Password must be at least 8 characters!", 404)

        else:
            query = "INSERT INTO Voter(first_name, last_name, gov_id, password, constituency_id, email) " \
                    "VALUES(?, ?, ?, ?, ?, ?)"
            cursor.execute(query, [fn, ln, gid, pw, c_id, email])

    return make_response(jsonify(cursor.commit()), 201)


def jwt_required(func):
    @wraps(func)
    def jwt_required_wrapper(*args, **kwargs):

        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.secret_key)
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return func(*args, **kwargs)

    return jwt_required_wrapper


@app.route("/api/v1.0/login", methods=["GET"])
def login():
    auth = request.authorization
    if auth:
        cursor.execute("SELECT * FROM Voter WHERE gov_id = ?", auth.username)
        for user in cursor.fetchall():
            hashed_password = bcrypt.hashpw(user[4].encode('utf8'), bcrypt.gensalt())
            if bcrypt.checkpw(bytes(auth.password, 'UTF-8'), hashed_password):
                token = jwt.encode(
                    {'user': auth.username,
                     'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                     }, app.secret_key)
                return make_response(jsonify({'token': token.decode('UTF-8')}), 200)
            else:
                return make_response(jsonify({'message': 'Bad password'}), 401)
        else:
            return make_response(jsonify({'message': 'Bad username'}), 401)

    return make_response(jsonify({'message': 'Authentication required'}), 401)


@app.route("/api/v1.0/logout", methods=["GET"])
@jwt_required
def logout():
    token = request.headers['x-access-token']
    blacklist.insert_one({"token": token})
    return make_response(jsonify({'message': 'Logout successful'}), 200)


@app.route("/api/v1.0/parties", methods=["GET"])
def show_all_parties():
    data_to_return = []
    query = "SELECT * FROM Party"
    cursor.execute(query)
    for row in cursor.fetchall():
        item_dict = {"party_id": row[0], "party_name": row[1], "image": row[2], "manifesto": row[3]}
        data_to_return.append(item_dict)
    return make_response(jsonify(data_to_return), 200)


def add_party():
    if "party_name" in request.form \
            and "image" in request.form \
            and "manifesto" in request.form:
        pn = request.form["party_name"]
        im = request.form["image"]
        ma = request.form["manifesto"]

        cursor.execute('SELECT * FROM Party WHERE party_name = ?', (pn,))
        party = cursor.fetchone()
        if party:
            return make_response("Party already exists!", 403)

        elif not pn or not im or not ma:
            return make_response("Please complete form", 404)

        else:
            query = "INSERT INTO Party(party_name, image, manifesto) " \
                    "VALUES(?, ?, ?)"
            cursor.execute(query, [pn, im, ma])

    return make_response(jsonify(cursor.commit()), 201)


@app.route("/api/v1.0/parties/<id>", methods=["GET"])
def show_one_party(id):
    data_to_return = []
    query = "SELECT * FROM Party WHERE party_id = ?"
    cursor.execute(query, (id,))
    for row in cursor.fetchall():
        item_dict = {"party_id": row[0], "party_name": row[1], "image": row[2], "manifesto": row[3]}
        data_to_return.append(item_dict)
    return make_response(jsonify(data_to_return), 200)


@app.route("/api/v1.0/parties/<id>", methods=["PUT"])
def edit_party(id):
    if "party_name" in request.form \
            and "image" in request.form \
            and "manifesto" in request.form:
        pn = request.form["party_name"]
        im = request.form["image"]
        ma = request.form["manifesto"]

        cursor.execute('SELECT * FROM Party WHERE party_name = ?', (pn,))
        party = cursor.fetchone()
        if party:
            return make_response("Party already exists!", 403)

        elif not pn or not im or not ma:
            return make_response("Please complete form", 404)

        else:
            query = 'UPDATE Party ' \
                    'SET party_name, image, manifesto = ?, ?, ? ' \
                    'WHERE party_id = ?'
            cursor.execute(query, [pn, im, ma, id])
            cursor.commit()

    return make_response(jsonify(cursor.commit()), 201)


def delete_party():
    return 0


@app.route("/api/v1.0/candidates/<id>", methods=["PUT"])
def edit_candidate(id):
    if "candidate_firstname" in request.form \
            and "candidate_lastname" in request.form \
            and "party_id" in request.form \
            and "image" in request.form \
            and "constituency_id" in request.form \
            and "statement" in request.form:
        fn = request.form["candidate_firstname"]
        ln = request.form["candidate_lastname"]
        p_id = request.form["party_id"]
        im = request.form["image"]
        c_id = request.form["constituency_id"]
        rq = request.form["request"]

        query = 'UPDATE Candidate ' \
                'SET candidate_firstname, candidate_lastname, party_id, image, constituency_id, statement = ?, ?, ?, ?, ?, ?' \
                'WHERE candidate_id = ?'
        cursor.execute(query, [fn, ln, p_id, im, c_id, rq, id])

    return make_response(jsonify(cursor.commit()), 201)


@app.route("/api/v1.0/candidates", methods=["POST"])
def add_candidate():
    if "candidate_firstname" in request.form \
            and "candidate_lastname" in request.form \
            and "party_id" in request.form \
            and "image" in request.form \
            and "constituency_id" in request.form \
            and "statement" in request.form:
        fn = request.form["candidate_firstname"]
        ln = request.form["candidate_lastname"]
        p_id = request.form["party_id"]
        im = request.form["image"]
        c_id = request.form["constituency_id"]
        rq = request.form["request"]

        query = "INSERT INTO Candidate(candidate_firstname, candidate_lastname, party_id, image, constituency_id, statement) " \
                "VALUES(?, ?, ?, ?, ?, ?)"
        cursor.execute(query, [fn, ln, p_id, im, c_id, rq])

    return make_response(jsonify(cursor.commit()), 201)


def delete_candidate():
    return 0


@app.route("/api/v1.0/candidates", methods=["GET"])
def show_all_candidates():
    data_to_return = []
    query = "SELECT * FROM Candidate"
    cursor.execute(query)
    for row in cursor.fetchall():
        item_dict = {"candidate_id": row[0], "candidate_firstname": row[1], "candidate_lastname": row[2]}
        data_to_return.append(item_dict)
    return make_response(jsonify(data_to_return), 200)


@app.route("/api/v1.0/candidates/<id>", methods=["GET"])
def show_one_candidate(id):
    data_to_return = []
    query = "SELECT * FROM Candidate WHERE candidate_id = ?"
    cursor.execute(query, id)
    for row in cursor.fetchall():
        item_dict = {"candidate_id": row[0], "candidate_firstname": row[1], "candidate_lastname": row[2]}
        data_to_return.append(item_dict)
    return make_response(jsonify(data_to_return), 200)


@app.route("/api/v1.0/voters/<id>", methods=["POST"])
def update_password(id):
    if "password" in request.form:
        pw = request.form["password"]

        if len(pw) < 8:
            return make_response("Password must be at least 8 characters!", 404)
        else:
            query = 'UPDATE Voter SET password = ? WHERE voter_id = ?'
            cursor.execute(query, [pw, id])
            cursor.commit()

    return make_response("Password successfully updated!", 200)


def gov_id_generator(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


if __name__ == "__main__":
    app.run(debug=True)
