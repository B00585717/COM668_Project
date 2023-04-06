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
from Models import Voter, Verification, Party, Candidate, engine, Constituency, Votes

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
        hashed_pw = encrypt_password(password)
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

            return make_response(jsonify({"message": "Success", "gov_id": new_voter.gov_id}), 201)

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
        # OTP = generate_otp()

        # TODO: This is just for testing, the application will use randomly generated otp's
        OTP = '123456'

        # Use GoogleAPI to send email containing otp
        send_otp(email, OTP)

        user = session.query(Verification).filter_by(email=email).first()

        if user:
            # New otp will overwrite old one to prevent duplicate entries
            session.query(Verification).filter_by(email=email).update({'otp': OTP})
            session.commit()

        else:
            # Save the OTP and email as a temporary registration record
            session.add(Verification(email=email, otp=OTP))
            session.commit()

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
        if check_password(password, user.get_password()):
            access_token = create_access_token(identity=gov_id)

            user_data = {
                'voter_id': user.voter_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'gov_id': user.gov_id,
                'email': user.email,
                'constituency_id': user.constituency_id
            }

            # Return access token
            return jsonify({'access_token': access_token, 'user_data': user_data})
        else:
            return jsonify({'message': 'Incorrect password.'}), 401
    else:
        return jsonify({'message': 'User not found.'}), 404


@app.route('/api/v1.0/profile', methods=["GET"])
@jwt_required()
def profile():
    gov_id = get_jwt_identity()

    user = session.query(Voter, Constituency.constituency_name) \
        .join(Constituency, Voter.constituency_id == Constituency.constituency_id) \
        .filter(Voter.gov_id == gov_id) \
        .first()

    if user is None:
        return jsonify({"message": "User not found"}), 404

    voter, constituency_name = user

    return jsonify({'first_name': voter.first_name,
                    'last_name': voter.last_name,
                    'gov_id': voter.gov_id,
                    'constituency_name': constituency_name,
                    'email': voter.email})


@app.route("/api/v1.0/parties", methods=["GET"])
def show_all_parties():
    parties = session.query(Party).all()

    party_list = []
    for party in parties:
        item_dict = {"party_id": party.party_id,
                     "party_name": party.party_name,
                     "image": party.image,
                     "manifesto": party.manifesto}
        party_list.append(item_dict)
    return make_response(jsonify(party_list), 200)


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


@app.route("/api/v1.0/parties", methods=["POST"])
def add_party():
    if "party_name" in request.form \
            and "image" in request.form \
            and "manifesto" in request.form:
        pn = request.form["party_name"]
        im = request.form["image"]
        ma = request.form["manifesto"]

        party = session.query(Party).filter_by(party_name=pn).first()
        if party:
            return make_response("Party already exists!", 403)

        elif not pn or not im or not ma:
            return make_response("Please complete form", 404)

        else:
            new_party = Party(
                party_name=pn,
                image=im,
                manifesto=ma
            )

            session.add(new_party)
            session.commit()

        return make_response(jsonify({"message": "Party created", "party_id": new_party.party_id}), 201)


@app.route("/api/v1.0/parties/<id>", methods=["PUT"])
def edit_party(id):
    if "party_name" in request.form \
            and "image" in request.form \
            and "manifesto" in request.form:
        pn = request.form["party_name"]
        im = request.form["image"]
        ma = request.form["manifesto"]

        party = session.query(Party).filter_by(party_name=pn).first()
        if party:
            return make_response("Party already exists!", 403)

        elif not pn or not im or not ma:
            return make_response("Please complete form", 404)

        else:
            party = session.query(Party).filter_by(party_id=id).first()
            if not party:
                return make_response("Party not found", 404)

            party.party_name = pn
            party.image = im
            party.manifesto = ma

            session.commit()

        return make_response(jsonify("Party updated"), 200)
    else:
        return make_response("Invalid request", 400)


@app.route("/api/v1.0/parties/<id>", methods=["DELETE"])
def delete_party(id):
    party = session.query(Party).filter_by(party_id=id).first()

    if not party:
        return make_response('Party not found', 404)

    session.delete(party)
    session.commit()

    return make_response('Party deleted', 200)


@app.route("/api/v1.0/candidates", methods=["GET"])
def show_all_candidates():
    data_to_return = []
    query = session.query(Candidate, Party.party_name) \
        .select_from(Candidate) \
        .join(Party, Candidate.party_id == Party.party_id) \
        .all()

    for candidate, party_name in query:
        item_dict = {
            "candidate_id": candidate.candidate_id,
            "candidate_firstname": candidate.candidate_firstname,
            "candidate_lastname": candidate.candidate_lastname,
            "party_id": candidate.party_id,
            "image": candidate.image,
            "statement": candidate.statement,
            "party_name": party_name
        }
        data_to_return.append(item_dict)

    return make_response(jsonify(data_to_return), 200)


@app.route("/api/v1.0/candidates/<id>", methods=["GET"])
def show_one_candidate(id):
    data_to_return = []
    query = "SELECT Candidate.*,Party.party_name, Party.image, Constituency.constituency_name " \
            "FROM Candidate " \
            "JOIN Party ON " \
            "Candidate.party_id=party.party_id JOIN Constituency ON Candidate.constituency_id = Constituency.constituency_id WHERE candidate_id = ?"
    cursor.execute(query, id)
    for row in cursor.fetchall():
        item_dict = {"candidate_id": row[0],
                     "candidate_firstname": row[1],
                     "candidate_lastname": row[2],
                     "party_id": row[3],
                     "image": row[5],
                     "statement": row[7],
                     "party_name": row[8],
                     "party_image": row[9],
                     "constituency_name": row[10]}
        data_to_return.append(item_dict)
    return make_response(jsonify(data_to_return), 200)


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
        st = request.form["statement"]

        candidate = session.query(Candidate).filter_by(candidate_id=id).first()
        if not candidate:
            return make_response("Candidate not found", 404)

        elif not fn or not ln or not c_id or not p_id or not im or not st:
            return make_response("Please complete form", 404)

        candidate.candidate_firstname = fn
        candidate.candidate_lastname = ln
        candidate.party_id = p_id
        candidate.image = im
        candidate.constituency_id = c_id
        candidate.statement = st

        session.commit()

    return make_response(jsonify("Candidate updated"), 200)


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

        candidate = session.query(Candidate).filter_by(candidate_lastname=ln).first()
        if candidate:
            return make_response("Candidate already exists!", 403)

        elif not fn or not ln or not c_id or not p_id or not im or not st:
            return make_response("Please complete form", 404)

        else:
            new_candidate = Candidate(
                candidate_firstname=fn,
                candidate_lastname=ln,
                party_id=p_id,
                image=im,
                constituency_id=c_id,
                statement=st)

            session.add(new_candidate)
            session.commit()

            return make_response(jsonify({"message": "Candidate added", "candidate_id": new_candidate.candidate_id}), 201)
    else:
        return make_response("Invalid request", 400)


@app.route("/api/v1.0/candidates/<id>", methods=["DELETE"])
def delete_candidate(id):
    candidate = session.query(Candidate).filter_by(candidate_id=id).first()

    if not candidate:
        return make_response("Candidate not found", 404)

    session.delete(candidate)
    session.commit()

    return make_response('Candidate deleted', 200)


@app.route("/api/v1.0/voters", methods=["GET"])
def show_all_voters():
    voters = session.query(Voter).all()

    data_to_return = []
    for voter in voters:
        item_dict = {
            "voter_id": voter.voter_id,
            "first_name": voter.first_name,
            "last_name": voter.last_name,
            "gov_id": voter.gov_id,
            "password": voter.password,
            "email": voter.email
        }
        data_to_return.append(item_dict)

    return make_response(jsonify(data_to_return), 200)


@app.route("/api/v1.0/profile/<g_id>", methods=["PUT"])
def update_password(g_id):
    if "password" in request.form:
        pw = request.form["password"]

        voter = session.query(Voter).filter_by(gov_id=g_id).first()

        if not voter:
            return make_response("User not found!", 404)

        if len(pw) < 8:
            return make_response("Password must be at least 8 characters!", 404)

        voter.password = encrypt_password(pw)
        session.commit()

        return jsonify({"message": "Password successfully updated!"}), 200
    else:
        return jsonify({"message": "Password field is missing in the request."}), 400


@app.route("/api/v1.0/profile/<g_id>", methods=["DELETE"])
def delete_voter(g_id):
    user = session.query(Voter).filter_by(gov_id=g_id).first()

    if not user:
        return make_response("User not found", 404)

    session.delete(user)
    session.commit()

    return make_response('User deleted', 200)


@app.route("/api/v1.0/votes", methods=["POST"])
def submit_vote():
    if "voter_id" in request.json and "candidate_id" in request.json:
        voter_id = request.json["voter_id"]
        candidate_id = request.json["candidate_id"]

        # Check if the user has already voted
        existing_vote = session.query(Votes).filter_by(voter_id=voter_id).first()
        if existing_vote:
            return make_response(jsonify({"message": "User has already voted"}), 403)

        # Check if the candidate exists
        candidate = session.query(Candidate).filter_by(candidate_id=candidate_id).first()
        if not candidate:
            return make_response(jsonify({"message": "Candidate not found"}), 404)

        # Create a new Vote object and store it in the database
        new_vote = Votes(voter_id=voter_id, candidate_id=candidate_id)
        session.add(new_vote)

        candidate.vote_count = get_vote_count(candidate_id) if candidate.vote_count else 1

        session.commit()

        return make_response(jsonify({"message": "Vote submitted", "vote_id": new_vote.vote_id}), 201)
    else:
        print("Invalid request:", request.json)
        return make_response(jsonify({"message": "Invalid request"}), 400)


@app.route("/api/v1.0/votes/<vote_id>", methods=["DELETE"])
def delete_vote(vote_id):
    vote = session.query(Votes).filter_by(vote_id=vote_id).first()
    if vote:
        candidate_id = vote.candidate_id
        session.delete(vote)
        session.commit()

        # Update the vote count for the candidate
        vote_count = get_vote_count(candidate_id)
        candidate = session.query(Candidate).filter_by(candidate_id=candidate_id).first()
        if candidate:
            candidate.vote_count = vote_count
            session.commit()

        return make_response(jsonify({"message": "Vote deleted", "vote_id": vote_id}), 200)
    else:
        return make_response(jsonify({"message": "Vote not found"}), 404)


@app.route("/api/v1.0/votes", methods=["DELETE"])
def reset_election():
    # Delete all vote entries
    session.query(Votes).delete()
    session.commit()

    # Update the vote_count for all candidates
    candidates = session.query(Candidate).all()
    for candidate in candidates:
        candidate.vote_count = 0
        session.commit()

    return make_response(jsonify({"message": "Election Reset"}), 200)

########## HELPER FUNCTIONS ##########

def encrypt_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def get_vote_count(candidate_id):
    return session.query(Votes).filter_by(candidate_id=candidate_id).count()


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
    temp_registration = session.query(Verification).filter_by(email=email, otp=otp).first()
    if temp_registration:
        return True
    return False


def user_exists(email):
    user = session.query(Voter).filter_by(email=email).first()
    if user:
        return True
    return False


def get_user_by_gov_id(gov_id):
    return session.query(Voter).filter_by(gov_id=gov_id).first()


def get_user_by_email(email):
    return session.query(Voter).filter_by(email=email).first()


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def send_otp(email, otp):
    email_sent = GoogleAPI.send_message(GoogleAPI.service, email, "Your OTP", f"Your OTP is: {otp}")
    if not email_sent:
        return make_response("Failed to send email", 500)


if __name__ == "__main__":
    app.run(debug=True)
