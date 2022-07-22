from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt
from flask_app import app

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db_name = "recipes_schema"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    @classmethod
    def register(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if not result:
            return False

        for row in result:
            user = cls(row)
        return user

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if not result:
            return False

        for row in result:
            user = cls(row)
        return user

    @staticmethod
    def validate_user_reg(user):
        is_valid = True
        result = User.get_user_by_email(user)
        if len(user['first_name']) < 2:
            flash("First name should have at least two characters")
            is_valid = False

        if len(user['last_name']) < 2:
            flash("First name should have at least two characters")
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email!")
            is_valid = False
        
        if EMAIL_REGEX.match(user['email']) and result and result.email != "":
            flash("A user with this email already exists")
            is_valid = False

        if len(user['password']) < 8 or not re.search(r"[\d]+", user['password']) or not re.search(r"[A-Z]+", user['password']):
            flash("Password should have at least eight characters, one digit and one capital letter!")
            is_valid = False

        if user['password'] and user['cpassword'] and user['password'] != user['cpassword']:
            flash("Passwords must match!")
            is_valid = False
        return is_valid
        
    @staticmethod
    def validate_user_log(user):
        is_valid = True
        user_by_email = User.get_user_by_email(user)

        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email!")
            is_valid = False

        if not user_by_email:
            flash("This email does not exist")
            is_valid = False
        
        if len(user['password']) < 8:
            flash("Password should have at least eight characters")
            is_valid = False

        if user_by_email and len(user['password']) >= 8 and user_by_email.password and not bcrypt.check_password_hash(user_by_email.password, user['password']):
            flash("Email or password is incorrect!")
            is_valid = False

        return is_valid
