from movies_app.config.mysqlconnection import connectToMySQL
from movies_app.models import user
from flask import flash

class Movie: 
    db ="movies_project"
    def __init__(self, db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.director = db_data['director']
        self.studio = db_data['studio']
        self.genre = db_data['genre']
        self.synopsis = db_data['synopsis']
        self.year = db_data['year']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.liked_by = []
        self.total_movies = 0

    # GET ALL
    @classmethod
    def get_all(cls):
        query ="""
                SELECT * FROM movies
                ORDER BY year ASC;
                """
        results = connectToMySQL(cls.db).query_db(query)
        for row in results: 
            these_movies = cls(row)
            movie_data = {
                'id': row['id'],
                'title': row['title'], 
                'director': row['director'],
                'studio': row['studio'], 
                'genre': row['genre'],
                'synopsis': row['synopsis'],
                'year': row['year'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
        return results
    
    @classmethod 
    def movies_count(cls):
        query = """
                SELECT COUNT(*) as count
                FROM movies;
                """
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        return results
    
    #GET BY ID
    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM movies
                LEFT JOIN likes ON movies.id = likes.movie_id
                LEFT JOIN users ON users.id = likes.user_id
                WHERE movies.id = %(id)s
                ORDER BY likes.created_at DESC;
                """
        results = connectToMySQL(cls.db).query_db(query,data)
        movie = cls(results[0])
        for row in results:
            if row['users.id'] == None:
                break
            data = {
                "id": row['users.id'],
                "user_name": row['user_name'],
                "email": row['email'],
                "password": "",
                "real_name": row['real_name'],
                "gender": row['gender'],
                "bio": row['bio'],
                "created_at": row['created_at'],
                "updated_at": row["updated_at"]
            }
            movie.liked_by.append(user.User(data))
        return movie

    #GET BY GENRE
    @classmethod
    def get_by_genre(cls,genre):
        data = {'genre':genre}
        query = """
                SELECT * FROM movies
                WHERE genre = %(genre)s
                ORDER BY year ASC;
                """
        results = connectToMySQL('movies_project').query_db(query, data)
        if not results:
            return False
        return results
    
    #GET BY YEAR
    @classmethod 
    def get_by_year(cls,year):
        data = {'year':year}
        query = """
                SELECT * FROM movies 
                WHERE year = %(year)s;
                """
        results = connectToMySQL(cls.db).query_db(query,data)
        if not results: 
            return False
        print(results)
        return results

    #GET BY USER LIKES
    @classmethod
    def movies_liked_by_user(cls):
        query ="""
                SELECT title FROM movies
                WHERE users.id = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query)
        liked_movies = []
        for row in results:
            liked_movies.append(cls(row))
        print(liked_movies)
        return liked_movies

    #ADD MOVIE
    @classmethod
    def save(cls, form_data):
        query ="""
                INSERT INTO movies (title, director, studio, genre, synopsis, year)
                VALUES (%(title)s, %(director)s, %(studio)s, %(genre)s, %(synopsis)s, %(year)s);
            """
        print(query)
        results = connectToMySQL(cls.db).query_db(query, form_data)
        print(results)
        return results
    
    #EDIT MOVIE
    @classmethod
    def update_movie(cls, form_data):
        query = """
                UPDATE movies
                SET title = %(title)s,
                director = %(director)s,
                studio = %(studio)s,
                genre = %(genre)s,
                synopsis = %(synopsis)s,
                year = %(year)s,
                updated_at = NOW()
                WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db).query_db(query, form_data)
    
    #DELETE MOVIE
    @classmethod
    def eliminate(cls,data):
        query="""
                DELETE FROM movies
                where id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)
    
    # MOVIE VALIDATION 
    @staticmethod 
    def validate_movie(movie):
        is_valid = True
        query = """
                SELECT * FROM movies 
                WHERE title = %(title)s
                AND year = %(year)s;
                """
        results = connectToMySQL(Movie.db).query_db(query, movie)

        if len(results) >= 1:
            flash("Movie is already part of our database")
            is_valid = False

        if len(movie['title']) < 1:
            flash("Must provide a title")
            is_valid = False
        
        if len(movie['director']) < 3:
            flash("Must name the film's director")
            is_valid = False
        
        if len(movie['genre']) < 5:
            flash("Must provide a genre")
            is_valid = False
        
        if len(movie['year']) < 4:
            flash("Must provide a valid year of release")
            is_valid = False

        return is_valid