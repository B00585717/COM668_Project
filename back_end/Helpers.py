import json
import random
import re
import bcrypt
from flask import make_response
from flask_jwt_extended import get_jwt_identity, jwt_required
from back_end import GoogleAPI
from back_end.API import postcode_regex
from back_end.Models import Voter, Verification, Votes

OTP_RANGE_MIN = 100000
OTP_RANGE_MAX = 999999


def encrypt_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def get_vote_count(candidate_id, session):
    return session.query(Votes).filter_by(candidate_id=candidate_id).count()


def gov_id_generator(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return random.randint(range_start, range_end)


def match_postcode_with_constituency(postcode):
    # Load the JSON dictionary from a file
    with open('constituencies.json', 'r') as constituencies:
        constituency_dictionary = json.load(constituencies)

    # Look up the value in the dictionary
    if postcode in constituency_dictionary:
        return constituency_dictionary[postcode]
    else:
        return None


def generate_otp():
    return str(random.randint(OTP_RANGE_MIN, OTP_RANGE_MAX))


def validate_email(email):
    # Regular expression for a properly constructed email address
    email_regex = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'

    if re.match(email_regex, email):
        return True
    else:
        return False


def validate_postcode(postcode):
    if re.search(postcode_regex, postcode):
        return True
    else:
        return False


def verify_otp(email, otp, session):
    registration = session.query(Verification).filter_by(email=email, otp=otp).first()
    if registration:
        return True
    else:
        return False


def user_exists(email, session):
    user = session.query(Voter).filter_by(email=email).first()
    if user:
        return True
    return False


def get_user_by_gov_id(gov_id, session):
    return session.query(Voter).filter_by(gov_id=gov_id).first()


def get_user_by_email(email, session):
    return session.query(Voter).filter_by(email=email).first()


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def send_otp(email, otp):
    email_sent = GoogleAPI.send_message(GoogleAPI.service, email, "Your OTP", f"Your OTP is: {otp}")
    if not email_sent:
        return make_response("Failed to send email", 500)


def send_gov_id(email, gov_id):
    email_sent = GoogleAPI.send_message(GoogleAPI.service, email, "Your Government ID",
                                        f"Your Government ID is: {gov_id}")
    if not email_sent:
        return make_response("Failed to send email", 500)


@jwt_required()
def get_user_from_request(session):
    gov_id = get_jwt_identity()

    user = get_gov_id(gov_id, session)
    return user


def get_gov_id(gov_id, session):
    return session.query(Voter).filter_by(gov_id=gov_id).first()


def get_password(gov_id, session):
    voter = session.query(Voter).filter_by(gov_id=gov_id).first()
    return voter.password