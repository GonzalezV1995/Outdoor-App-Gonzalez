from flask_app.config.mysqlconnection import connectToMySQL
# from pprint import pprint
from flask import flash, request
from flask_app import bcrypt
import re	# the regex module

# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
mysqlconnection = "flaskposts"
db = "outdoor_app_schema"
class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email'] # ask if its email or email address
        self.city = data['city']
        self.state = data['state']
        self.password = data['password']
        # self.created_at = data['created_at']
        # self.updated_at = data['updated_at']


    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(db).query_db(query)

        users=[]

        for user in results:
            users.append(cls(user))

        return users

    @classmethod
    def get_email(cls, data):

        query = "SELECT * FROM users WHERE email = %(email)s;"

        result = connectToMySQL(db).query_db(query, data)
        return cls(result[0]) if result else None

    @classmethod
    def get_id(cls, data):

        query = "SELECT * FROM users WHERE id = %(id)s;"

        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0]) if results else None

    @staticmethod
    def validate_registration(user_information):
        is_valid = True
        
        data = {
            'email': request.form['email']
        }
        if len(user_information['first_name']) <= 1:
            flash('First name required!', 'register')
            is_valid = False

        if len(user_information['last_name']) <= 0:
            flash('Last name required!', 'register')
            is_valid = False

        if len(user_information['email']) <= 0:
            flash('Email required!', 'register')
            is_valid = False

        if not EMAIL_REGEX.match(user_information['email']):
            flash('Invalid Email Address', 'register')
            is_valid = False

        if len(user_information['city']) <= 0:
            flash('City required!', 'register')
            is_valid = False

        if len(user_information['state']) <= 0:
            flash('State required!', 'register')
            is_valid = False

        if len(user_information['password']) <= 5:
            flash('Password must be at least 5 characters', 'register')
            is_valid = False

        if user_information['password'] != user_information['confirm_password']:
            flash('Passwords need to match', 'register')
            is_valid = False        
        
        if not EMAIL_REGEX.match(user_information['email']):
            flash('Invalid credentials','login')
            return False

        if User.get_email(data):
            flash('Email already taken', 'register')
            is_valid = False

        print('Validation: User is valid: ', is_valid)

        return is_valid

    # ------------------------------

    @classmethod # this saves the data and updates the database with new information
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password, city, state) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(city)s, %(state)s);'

        return connectToMySQL("outdoor_app_schema").query_db(query, data)

    # ------------------------------
