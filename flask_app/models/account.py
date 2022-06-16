from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$')

class Account:
    db = "accounts_schema"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls,data):
        query = "INSERT INTO accounts (first_name, last_name, email, password, created_at, updated_at ) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s , NOW() , NOW());"
        result = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        return result
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM accounts;"
        result = connectToMySQL(cls.db).query_db(query)
        all_account = []
        for row in result:
            all_account.append(cls(row))
        return all_account
    
    @classmethod
    def remove(cls,data):
        query = "DELETE FROM accounts WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM accounts WHERE email =%(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        if len(result) < 1:
            return False
        this_account = cls(result[0])
        return this_account

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM accounts WHERE id =%(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        if len(result) < 1:
            return False
        this_account = cls(result[0])
        return this_account

    @staticmethod
    def validate_register( account ):
        is_valid = True
        query = "SELECT * FROM accounts WHERE email = %(email)s;"
        result = connectToMySQL(Account.db).query_db(query,account)
        if len(result) >=1:
            flash("Email already taken.","register")
            is_valid = False
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(account['email']):
            flash("Invalid Email","register") 
            is_valid = False
        if len(account['first_name']) < 2:
            flash("First name must be at least 2 characters.","register")
            is_valid = False
        if len(account['last_name']) < 2:
            flash("Last name must be at least 2 characters.","register")
            is_valid = False
        if not PASSWORD_REGEX.match(account['password']):
            flash("Password must be at least 1 number and 1 uppercase","register") 
            is_valid = False    
        # if len(account['password']) < 8:
        #     flash("Password must be at least 8 characters.","register")
        #     is_valid = False
        if not (account['password']) == (account['confirm_pass']):
            flash("Passwords don't match","register")
            is_valid = False
        return is_valid