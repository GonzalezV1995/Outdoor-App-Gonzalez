from flask_app.config.mysqlconnection import connectToMySQL
#in the class apps you need this ^ written from folder to file 
from flask import flash, request
from flask_app.models import user

class Activites:
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.user_id = data['user_id']
        self.current_user = None

    @staticmethod
    def validate_comment(data): # need backend 
        is_valid = True

        
        if len(data['location']) < 3:
            flash("Location at least 3 characters long.")
            is_valid = False

        if len(data['description']) < 3:
            flash("Description at least 3 characters long.")
            is_valid = False
        
        print('Validation: User is valid: ', is_valid)
        return is_valid

    @classmethod 
    def get_all(cls):
        query = "SELECT * FROM activities JOIN users on activities.user_id = users.id;"
        results = connectToMySQL("outdoor_app_schema").query_db(query)

        comments=[]

        for row in results:
            comment = cls(row)
            user_information = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'city': row['city'],
                'state': row['state'],
                'password': row['password'],
            }
            comment.current_user = user.User(user_information)
            comments.append(comment)

        return comments
# --------------------------


    @classmethod
    def get_id(cls, data):
        query = "SELECT * FROM activities JOIN users on activities.user_id = users.id WHERE activities.id = %(id)s;"

        result = connectToMySQL("outdoor_app_schema").query_db(query, data)
        if not result:
            return False
        
        result = result[0]
        comment = cls(result)

        user_information = {
                'id': result['users.id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'city': result['city'],
                'state': result['state'],
                'email': result['email'],
                'password': result['password']
            }
        comment.current_user = user.User(user_information)
        return comment
    @classmethod
    def delete_comment(cls,data):
        query = "DELETE FROM `activities` WHERE id =%(id)s"
        return connectToMySQL('outdoor_app_schema').query_db(query, data)
# ------------------------------
    @classmethod
    def update_comment(cls,data):
        query = 'UPDATE activities SET location = %(location)s, description = %(description)s WHERE id = %(id)s;'
        return connectToMySQL('outdoor_app_schema').query_db(query,data)

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO activities ( location, description, user_id ) VALUES ( %(location)s, %(description)s, %(user_id)s);'
        return connectToMySQL('outdoor_app_schema').query_db(query,data)