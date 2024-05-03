from . import db
from .models import User
import re

class DisplayMessages:
    def green (self, message):
        return "Message.green(`{}`);".format(message)
    def red (self, message):
        return "Message.red(`{}`);".format(message)
    

class CheckCredentials (DisplayMessages):
    # def __init__(self):
    #     super().__init__()  # Call the __init__ method of the parent class
    #     pass

    
    def email (self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True
        else:
            return self.red("Email represented in invalid format!")


    
    
    def password(self, password):

        badPasswords = [
        "123456",
        "12345678",
        "123456789",
        "password",
        "Aa123456",
        "1234567890",
        "UNKNOWN",
        "1234567",
        "123123",
        "111111",
        "Password",
        "12345678910",
        "000000",
        "Admin123",
        "********",
        ]

        if (len(password) < 6 or password in badPasswords):
            return self.red ("Bad password!")
        return True
    

    
    def text (self, text):
        if (len(text) < 1):
            return self.red ("The text should be at least 1 character long!")
        return True
    
    def all(self, u_email, u_text, u_password):
        email = self.email(u_email)
        text = self.text(u_text)
        password = self.password(u_password)

        message = ""
        if type(email) == str:  # Check if email returned an error message (string)
            message += email
        if type(text) == str:
            message += text
        if type(password) == str:
            message += password

        if message:
            return message
        else:
            return True  #   All validations passed, return True
                
class CheckDB (DisplayMessages): 
    def email (self, eml):
        user = User.query.filter_by (email = eml).first()
        if (user):
            return self.red ("User already exists")
        else:
            return False

