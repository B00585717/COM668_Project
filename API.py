import random
import re
from sqlalchemy.orm import sessionmaker
import GoogleAPI
import bcrypt
from datetime import timedelta
from random import randint
from decouple import config
from flask import Flask, request, jsonify, make_response, json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from DBConfig import DBConfig
from flask_cors import CORS
from Models import Voter, Constituency, engine, Verification

app = Flask(__name__)
app.secret_key = config('SK')
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app)

jwt = JWTManager(app)
SQLdb = DBConfig()
cursor = SQLdb.get_cursor()

# Create a session factory
Session = sessionmaker(bind=engine)

# Use the session to interact with the database
session = Session()

# Constants
GOV_ID_LENGTH = 8
OTP_RANGE_MIN = 100000
OTP_RANGE_MAX = 999999
PASSWORD_LENGTH = 8

# Regular expression that takes the first part of postcode
postcode_regex = r'^[A-Z0-9]{3}([A-Z0-9](?=\s*[A-Z0-9]{3}|$))?'


@app.route("/api/v1.0/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        password = data.get("password")
        postcode = data.get("postcode")
        email = data.get("email")
        otp = data.get("otp")

        # Validation
        if not (first_name and last_name and password and postcode and email and otp):
            return make_response(jsonify({"message": "Missing required fields"}), 400)

        if not validate_email(email):
            return make_response(jsonify({"message": "Invalid email address"}), 400)

        if not validate_postcode(postcode):
            return make_response(jsonify({"message": "Invalid postcode"}), 400)

        if len(password) < PASSWORD_LENGTH:
            return make_response(jsonify({"message": "Password must be at least 8 characters!"}), 400)

        if not verify_otp(email, otp):
            return make_response(jsonify({"message": "Invalid OTP or email"}), 400)

        # All validations passed, proceed with registration

        # Password is hashed before it is inserted into database
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        c_id = match_postcode_with_constituency(re.search(postcode_regex, postcode).group(0))
        gov_id = gov_id_generator(GOV_ID_LENGTH)

        if user_exists(email):
            return make_response(jsonify({"message": "User already exists!"}), 403)
        else:
            new_voter = Voter(
                first_name=first_name,
                last_name=last_name,
                gov_id=gov_id,
                password=hashed_pw,
                constituency_id=c_id,
                email=email
            )

            # Add the new voter to the session
            session.add(new_voter)

            # Commit the session to save the new voter to the database
            session.commit()

            session.query(Verification).filter_by(email=email, otp=otp).delete()
            session.commit()

            return make_response(jsonify({"message": "Success"}), 201)

    except Exception as e:
        print(f"An error occurred: {e}")
        return make_response(jsonify("An error occurred", 500))


@app.route("/api/v1.0/verification", methods=["POST"])
def verification():
    try:
        request_data = request.get_json()
        email = request_data.get("email")

        user = get_user_by_email(email)

        if user:
            return make_response(jsonify({"message": "User already exists!"}), 403)

        # Generate a random 6-digit OTP
        OTP = generate_otp()

        # Use GoogleAPI to send email containing otp
        send_otp(email, OTP)

        user = session.query(Verification).filter_by(email=email).first()

        if user:
            # New otp will overwrite old one to prevent duplicate entries
            session.query(Verification).filter_by(email=email).update({'otp': OTP})
            session.commit()

        else:
            # Save the OTP and email as a temporary registration record
            query = "INSERT INTO Verification(email, otp) VALUES(?, ?)"
            cursor.execute(query, [email, OTP])
            cursor.commit()

        return make_response(jsonify({'message': 'OTP sent'}), 200)

    except Exception as e:
        print(f"An error occurred: {e}")
        return make_response("An error occurred", 500)


@app.route("/api/v1.0/login", methods=["POST"])
def login():
    gov_id = request.form['gov_id']
    password = request.form['password']

    user = get_user_by_gov_id(gov_id)

    # Check if the user was found in the database
    if user:
        if check_password(password, user[4]):
            access_token = create_access_token(identity=gov_id)
            # Return access token
            return jsonify({'access_token': access_token})
        else:
            return jsonify({'message': 'Incorrect password.'}), 401
    else:
        return jsonify({'message': 'User not found.'}), 404


@app.route('/api/v1.0/profile', methods=["GET"])
@jwt_required()
def profile():
    gov_id = get_jwt_identity()

    cursor.execute("SELECT Voter.*,Constituency.constituency_name "
                   "FROM Voter "
                   f"JOIN Constituency ON Voter.constituency_id=Constituency.constituency_id WHERE gov_id='{gov_id}'"
                   )

    user = cursor.fetchone()

    if user is None:
        return jsonify({"message": "User not found"}), 404

    return jsonify({'first_name': user[1],
                    'last_name': user[2],
                    'gov_id': user[3],
                    'constituency_name': user[7],
                    'email': user[6]})


@app.route("/api/v1.0/parties", methods=["GET"])
def show_all_parties():
    data_to_return = []
    query = "SELECT * FROM Party"
    cursor.execute(query)
    for row in cursor.fetchall():
        item_dict = {"party_id": row[0],
                     "party_name": row[1],
                     "image": row[2],
                     "manifesto": row[3]}
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
        item_dict = {"party_id": row[0],
                     "party_name": row[1],
                     "image": row[2],
                     "manifesto": row[3]}
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
    query = "SELECT Candidate.*,Party.party_name " \
            "FROM Candidate " \
            "JOIN Party ON " \
            "Candidate.party_id=party.party_id "
    cursor.execute(query)
    for row in cursor.fetchall():
        item_dict = {"candidate_id": row[0],
                     "candidate_firstname": row[1],
                     "candidate_lastname": row[2],
                     "party_id": row[3],
                     "image": row[5],
                     "statement": row[7],
                     "party_name": row[8]}
        data_to_return.append(item_dict)
    return make_response(jsonify(data_to_return), 200)


@app.route("/api/v1.0/voters", methods=["GET"])
def show_all_voters():
    data_to_return = []
    query = "SELECT * FROM Voter"
    cursor.execute(query)
    for row in cursor.fetchall():
        item_dict = {"voter_id": row[0],
                     "first_name": row[1],
                     "last_name": row[2],
                     "gov_id": row[3],
                     "password": row[4],
                     "email": row[6]}
        data_to_return.append(item_dict)
    return make_response(jsonify(data_to_return), 200)


@app.route("/api/v1.0/candidates/<id>", methods=["GET"])
def show_one_candidate(id):
    data_to_return = []
    query = "SELECT Candidate.*,Party.party_name, Party.image " \
            "FROM Candidate " \
            "JOIN Party ON " \
            "Candidate.party_id=party.party_id " \
            "WHERE candidate_id = ?"
    cursor.execute(query, id)
    for row in cursor.fetchall():
        item_dict = {"candidate_id": row[0],
                     "candidate_firstname": row[1],
                     "candidate_lastname": row[2],
                     "party_id": row[3],
                     "image": row[5],
                     "statement": row[7],
                     "party_name": row[8],
                     "party_image": row[9]}
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


def validate_email(email):
    # Regular expression for a properly constructed email address
    email_regex = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'

    if re.match(email_regex, email):
        return True
    return False


def validate_postcode(postcode):
    if re.search(postcode_regex, postcode):
        return True
    return False


def verify_otp(email, otp):
    cursor.execute('SELECT * FROM Verification WHERE email = ? AND otp = ?', (email, otp))
    temp_registration = cursor.fetchone()
    if temp_registration:
        return True
    return False


def user_exists(email):
    cursor.execute('SELECT * FROM Voter WHERE email = ?', (email,))
    user = cursor.fetchone()
    if user:
        return True
    return False


def get_user_by_gov_id(gov_id):
    cursor.execute(f"SELECT * FROM Voter WHERE gov_id='{gov_id}'")
    return cursor.fetchone()


def get_user_by_email(email):
    cursor.execute(f"SELECT * FROM Voter WHERE email='{email}'")
    return cursor.fetchone()


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def send_otp(email, otp):
    email_sent = GoogleAPI.send_message(GoogleAPI.service, email, "Your OTP", f"Your OTP is: {otp}")
    if not email_sent:
        return make_response("Failed to send email", 500)


if __name__ == "__main__":
    app.run(debug=True)
