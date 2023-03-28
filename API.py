import random
import re
import GoogleAPI
import bcrypt
from datetime import timedelta
from random import randint
from decouple import config
from flask import Flask, request, jsonify, make_response, json, session
from flask_jwt_extended import JWTManager
from DBConfig import DBConfig
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = config('SK')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
CORS(app)

jwt = JWTManager(app)
SQLdb = DBConfig()
cursor = SQLdb.get_cursor()

# Constants
GOV_ID_LENGTH = config('GID_LENGTH')
OTP_RANGE_MIN = config('OTP_MIN')
OTP_RANGE_MAX = config('OTP_MAX')
PASSWORD_LENGTH = config('PW_LENGTH')


# Regular expression for a properly constructed email address
email_regex = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'

# Regular expression that takes the first part of postcode
postcode_regex = r'^[A-Z0-9]{3}([A-Z0-9](?=\s*[A-Z0-9]{3}|$))?'


@app.route("/api/v1.0/register", methods=["POST"])
def register():
    try:
        if "first_name" in request.form \
                and "last_name" in request.form \
                and "password" in request.form \
                and "postcode" in request.form \
                and "email" in request.form:
            fn = request.form["first_name"]
            ln = request.form["last_name"]
            gid = gov_id_generator(GOV_ID_LENGTH)
            pw = request.form["password"]
            postcode = request.form["postcode"]
            email = request.form["email"]

            # Password is hashed before it is inserted into database
            hashed_pw = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())

            # Generate a random 6-digit OTP
            otp = generate_otp()

            cursor.execute('SELECT * FROM Voter WHERE email = ?', (email,))
            user = cursor.fetchone()
            if user:
                return make_response("User already exists!", 403)

            elif not re.match(email_regex, email):
                return make_response("Invalid email address", 404)

            elif not re.search(postcode_regex, postcode).group(0):
                return make_response('Invalid Postcode', 404)

            elif len(pw) < PASSWORD_LENGTH:
                return make_response("Password must be at least 8 characters!", 404)

            else:
                # Use GoogleAPI to send email containing otp
                email_sent = GoogleAPI.send_message(GoogleAPI.service, email, "Your OTP", f"Your OTP is: {otp}")

                if not email_sent:
                    return make_response("Failed to send email", 500)

                postcode = re.search(postcode_regex, postcode).group(0)
                c_id = match_postcode_with_constituency(postcode)

                # TODO: Current implementation of 2fa uses input from console to authenticate otp, will change later
                if input("Enter the OTP sent to your email: ") == otp:
                    query = "INSERT INTO Voter(first_name, last_name, gov_id, password, constituency_id, email) " \
                            "VALUES(?, ?, ?, ?, ?, ?)"
                    cursor.execute(query, [fn, ln, gid, hashed_pw, c_id, email])
                    cursor.commit()
                    return make_response('Success', 201)
                else:
                    return make_response('Invalid OTP', 404)
    except Exception as e:
        print(f"An error occurred: {e}")
        return make_response("An error occurred", 500)


@app.route("/api/v1.0/login", methods=["POST"])
def login():
    gov_id = request.form['gov_id']
    password = request.form['password']

    # Query the Azure SQL Database to check if the gov_id and password are correct
    cursor.execute(f"SELECT * FROM Voter WHERE gov_id='{gov_id}'")
    user = cursor.fetchone()

    # Check if the user was found in the database
    if user:
        hashed_password = user[4]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            # Store the user ID in the session
            session['user_id'] = user[0]
            # Return a success message
            return jsonify({'Success!': 200})
        else:
            return jsonify({'message': 'Incorrect password.'}), 401
    else:
        # Return an error message
        return jsonify({'message': 'User not found.'}), 404


@app.route('/profile')
def profile():
    # Check if the user is logged in
    if 'user_id' not in session:
        # Redirect to the login page if the user is not logged in
        return jsonify({'message': 'You must log in to view this page.'}), 401

    # Query the Azure SQL Database to get the user's profile information
    cursor.execute(f"SELECT * FROM Voter WHERE voter_id='{session['user_id']}'")
    user = cursor.fetchone()

    # Return the user's profile information
    return jsonify({'first name': user[1], 'last name': user[2]})


@app.route('/logout')
def logout():
    # Clear the user ID from the session
    session.pop('user_id', None)

    # Return a success message
    return jsonify({'message': 'Logout successful!'})


@app.route("/api/v1.0/parties", methods=["GET"])
def show_all_parties():
    data_to_return = []
    query = "SELECT * FROM Party"
    cursor.execute(query)
    for row in cursor.fetchall():
        item_dict = {"party_id": row[0], "party_name": row[1], "image": row[2], "manifesto": row[3]}
        data_to_return.append(item_dict)
    return make_response(jsonify(data_to_return), 200)


@app.route("/api/v1.0/parties", methods=["POST"])
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
        st = request.form["statement"]

        query = "INSERT INTO Candidate(candidate_firstname, candidate_lastname, party_id, image, constituency_id, statement) " \
                "VALUES(?, ?, ?, ?, ?, ?)"
        cursor.execute(query, [fn, ln, p_id, im, c_id, st])

    return make_response(jsonify(cursor.commit()), 201)


def delete_candidate():
    return 0


@app.route("/api/v1.0/candidates", methods=["GET"])
def show_all_candidates():
    data_to_return = []
    query = "SELECT * FROM Candidate"
    cursor.execute(query)
    for row in cursor.fetchall():
        item_dict = {"candidate_id": row[0], "candidate_firstname": row[1], "candidate_lastname": row[2],
                     "party_id": row[3], "image": row[5], "statement": row[7]}
        data_to_return.append(item_dict)
    return make_response(jsonify(data_to_return), 200)


@app.route("/api/v1.0/voters", methods=["GET"])
def show_all_voters():
    data_to_return = []
    query = "SELECT * FROM Voter"
    cursor.execute(query)
    for row in cursor.fetchall():
        item_dict = {"voter_id": row[0], "first_name": row[1], "last_name": row[2], "gov_id": row[3],
                     "password": row[4], "email": row[6]}
        data_to_return.append(item_dict)
    return make_response(jsonify(data_to_return), 200)


@app.route("/api/v1.0/candidates/<id>", methods=["GET"])
def show_one_candidate(id):
    data_to_return = []
    query = "SELECT * FROM Candidate WHERE candidate_id = ?"
    cursor.execute(query, id)
    for row in cursor.fetchall():
        item_dict = {"candidate_id": row[0], "candidate_firstname": row[1], "candidate_lastname": row[2],
                     "party_id": row[3], "image": row[5], "statement": row[7]}
        data_to_return.append(item_dict)
    return make_response(jsonify(data_to_return), 200)


@app.route("/api/v1.0/voters/<id>", methods=["PUT"])
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


########## HELPER FUNCTIONS ##########
def gov_id_generator(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def match_postcode_with_constituency(postcode):
    # Load the JSON dictionary from a file
    with open('constituencies.json', 'r') as f:
        my_dictionary = json.load(f)

    # Look up the value in the dictionary
    if postcode in my_dictionary:
        return my_dictionary[postcode]
    else:
        return None

def generate_otp():
    return str(random.randint(OTP_RANGE_MIN, OTP_RANGE_MAX))


if __name__ == "__main__":
    app.run(debug=True)
