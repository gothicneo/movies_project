from movies_app.config.mysqlconnection import connectToMySQL

from movies_app.models import user, movie

class Like: 
    db = "movies_project"
    def __init__(self, db_data):
        self.movie_id = db_data['movie_id']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']

    @classmethod
    def user_likes(cls):
        query ="""
                SELECT * FROM likes;
                """
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        return results

    @classmethod
    def create_like(cls, data):
        query = """
                INSERT INTO likes (movie_id, user_id)
                VALUES (%(movie_id)s, %(user_id)s);
                """
        connectToMySQL(cls.db).query_db(query, data)