import unittest
from unittest.mock import MagicMock

import bcrypt

import API
from API import encrypt_password, gov_id_generator, match_postcode_with_constituency, generate_otp, validate_email, \
    validate_postcode, verify_otp, user_exists, get_user_by_gov_id, get_user_by_email, check_password


class TestApp(unittest.TestCase):

    postcode_regex = API.postcode_regex

    def test_encrypt_password(self):
        password = "test_password"
        encrypted_password = encrypt_password(password)
        self.assertNotEqual(password, encrypted_password)

    def test_gov_id_generator(self):
        n = 6
        gov_id = gov_id_generator(n)
        self.assertEqual(n, len(str(gov_id)))

    def test_match_postcode_with_constituency_valid_postcode(self):
        postcode = "BT45"
        expected_constituency = 15

        constituency = match_postcode_with_constituency(postcode)
        self.assertEqual(constituency, expected_constituency)

    def test_match_postcode_with_constituency_invalid_postcode(self):
        postcode = "INVALID"

        constituency = match_postcode_with_constituency(postcode)
        self.assertIsNone(constituency)

    def test_otp_generator(self):
        n = 6
        otp = generate_otp()
        self.assertEqual(n, len(str(otp)))

    def test_otp_generator_is_6_digits(self):
        n = 7
        otp = generate_otp()
        self.assertNotEqual(n, len(str(otp)))

    def test_validate_email_valid_email(self):
        valid_email = "johnsmith@example.com"

        result = validate_email(valid_email)
        self.assertTrue(result)

    def test_validate_email_invalid_email(self):
        invalid_email = "johnsmith@example"

        result = validate_email(invalid_email)
        self.assertFalse(result)

    def test_validate_email_empty_string(self):
        empty_email = ""

        result = validate_email(empty_email)
        self.assertFalse(result)

    def test_validate_postcode_valid_postcode(self):
        valid_postcode = "AB10 1XG"

        result = validate_postcode(valid_postcode)
        self.assertTrue(result)

    def test_validate_postcode_invalid_postcode(self):
        invalid_postcode = "AB!34"

        result = validate_postcode(invalid_postcode)
        self.assertFalse(result)

    def test_validate_postcode_empty_string(self):
        empty_postcode = ""

        result = validate_postcode(empty_postcode)
        self.assertFalse(result)

    def test_verify_otp_valid(self):
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = {'email': 'johnsmith@example.com', 'otp': '123456'}

        with unittest.mock.patch('API.session.query', return_value=mock_query):
            result = verify_otp('', '123456')
            self.assertTrue(result)

    def test_verify_otp_invalid(self):
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = None

        with unittest.mock.patch('API.session.query', return_value=mock_query):
            result = verify_otp('johnsmith@example.com', '000000')
            self.assertFalse(result)

    def test_user_exists_true(self):
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = {'email': 'johnsmith@example.com'}

        with unittest.mock.patch('API.session.query', return_value=mock_query):
            result = user_exists('johnsmith@example.com')
            self.assertTrue(result)

    def test_user_exists_false(self):
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = None

        with unittest.mock.patch('API.session.query', return_value=mock_query):
            result = user_exists('notfound@example.com')
            self.assertFalse(result)

    def test_get_user_by_gov_id_found(self):
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = {'gov_id': '123456'}

        with unittest.mock.patch('API.session.query', return_value=mock_query):
            result = get_user_by_gov_id('123456')
            self.assertEqual(result, {'gov_id': '123456'})

    def test_get_user_by_gov_id_not_found(self):
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = None

        with unittest.mock.patch('API.session.query', return_value=mock_query):
            result = get_user_by_gov_id('NOTNUMBER')
            self.assertIsNone(result)


    def test_get_user_by_email_found(self):
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = {'email': 'johnsmith@example.com'}

        with unittest.mock.patch('API.session.query', return_value=mock_query):
            result = get_user_by_email('johnsmith@example.com')
            self.assertEqual(result, {'email': 'johnsmith@example.com'})

    def test_get_user_by_email_not_found(self):
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = None

        with unittest.mock.patch('API.session.query', return_value=mock_query):
            result = get_user_by_email('johnsmith@example.com')
            self.assertIsNone(result)

    def test_check_password_correct(self):
        password = 'test_password'
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        result = check_password(password, hashed_password.decode('utf-8'))
        self.assertTrue(result)

    def test_check_password_incorrect(self):
        password = 'test_password'
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        result = check_password('wrong_password', hashed_password.decode('utf-8'))
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
