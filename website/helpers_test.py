import unittest
from unittest.mock import patch
from helpers_for_testing import CheckCredentials, DisplayMessages

class TestCheckCredentials(unittest.TestCase):

    def setUp(self):
        self.check_cred = CheckCredentials()
        self.disp_msg = DisplayMessages ()

    def test_email_valid(self):
        self.assertTrue(self.check_cred.email('example@example.com'))

    def test_email_invalid_format(self):
        self.assertEqual(self.check_cred.email('invalid_email'), "Message.red(`Email represented in invalid format!`);")

    def test_password_bad(self):
        self.assertEqual(self.check_cred.password('password'), "Message.red(`Bad password!`);")

    def test_password_good(self):
        self.assertTrue(self.check_cred.password('good_password'))

    def test_text_short(self):
        self.assertEqual(self.check_cred.text(''), "Message.red(`The text should be at least 1 character long!`);")

    def test_text_long(self):
        self.assertTrue(self.check_cred.text('long enough text'))

    def test_all_valid(self):
        self.assertTrue(self.check_cred.all('example@example.com', 'some text', 'good_password'))

    def test_all_invalid(self):
        expected_message = "Message.red(`Email represented in invalid format!`);Message.red(`The text should be at least 1 character long!`);Message.red(`Bad password!`);"
        self.assertEqual(self.check_cred.all('invalid_email', '', 'password'), expected_message)



if __name__ == '__main__':
    unittest.main()