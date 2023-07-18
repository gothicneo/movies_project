from movies_app.config.mysqlconnection import connectToMySQL
from movies_app.models import movie
import re #Regex module
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from flask import flash

class User: 
    db = "movies_project"
    def __init__(self,data):
        self.id = data['id']
        self.user_name = data['user_name']
        self.email = data['email']
        self.password = data['password']
        self.real_name = data['real_name']
        self.gender = data['gender']
        self.bio = data['bio']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.total_movies = 0
        self.liked_movies = []
        self.likes = 0
    
    #GET ALL USERS
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        users = []
        results = connectToMySQL('movies_project').query_db(query)
        for row in results:
            users.append(cls(row))
        return users

    #GET USER BY ID
    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM users 
                LEFT JOIN likes ON users.id = likes.user_id 
                LEFT JOIN movies ON movies.id = likes.movie_id
                WHERE users.id = %(id)s
                ORDER BY likes.created_at DESC
                LIMIT 5;
                """
        results = connectToMySQL('movies_project').query_db(query,data)
        user = cls(results[0])
        for row in results:
            if row['movies.id'] == None:
                break
            data = {
                "id": row['movies.id'],
                "title": row['title'],
                "director": row['director'],
                "studio": row['studio'],
                "genre": row['genre'],
                "year": row['year'],
                "synopsis": row['synopsis'],
                "created_at": row['movies.created_at'],
                "updated_at": row['movies.updated_at']
            }
            user.liked_movies.append(movie.Movie(data))
        print(user.liked_movies)
        print(user.likes)
        return user
    
    #GET USER BY EMAIL
    @classmethod
    def get_email(cls,data):
        query ="""
                SELECT * FROM users 
                WHERE email = %(email)s;
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    #REGISTER USER
    @classmethod
    def register_user(cls,data):
        query = """
                INSERT INTO users(user_name, email, password)
                VALUES (%(user_name)s, %(email)s, %(password)s);
                """
        return connectToMySQL(cls.db).query_db(query,data)
    
    #EDIT USER 
    @classmethod
    def update_user(cls, form_data):
        query = """
                UPDATE users
                SET real_name = %(real_name)s,
                gender = %(gender)s,
                bio = %(bio)s,
                updated_at = NOW()
                WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db).query_db(query, form_data)
    
    #ADD LIKE 
    @classmethod
    def add_like(cls,data):
        query = """
                INSERT INTO likes (movie_id, user_id)
                VALUES (%(movie_id)s, %(user_id)s);
                """
        return connectToMySQL(cls.db).query_db(query,data)
    
    #VALIDATION
    @staticmethod
    def validate_reg(user):
        is_valid = True
        query = """
                SELECT * FROM users 
                WHERE email = %(email)s OR user_name = %(user_name)s;
                """
        results = connectToMySQL(User.db).query_db(query, user)

        if len(user['user_name']) < 3: 
            flash("User name must be longer than 3 characters", 'reg_error')
            is_valid = False

        if len(results) >= 1:
            flash("Email address or username is already registered", 'reg_error')
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address", 'reg_error')

        if len(user['password']) < 8:
            flash("Password must contain more than 8 characters", 'reg_error')
            is_valid = False
        
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match", 'reg_error')

        print(user['password'])
        print(is_valid)

        return is_valid 
    