from flask import Flask, render_template, session, redirect, request, flash
from movies_app.models.movie import Movie
from movies_app.models.user import User 
from movies_app.models.like import Like
from movies_app import app

@app.route('/movies')
def all_movies():
    if 'user_id' not in session: 
        log = "login"
        return redirect('/')
    else: 
        log = "logout"
    data ={
        'id': session['user_id']
    }
    return render_template('movies_all.html', movies=Movie.get_all(), user = User.get_by_id(data), log=log, total_movies=Movie.movies_count(), likes=Like.user_likes())

@app.route('/movies/submit')
def save_movie():
    if 'user_id' not in session: 
        log = "login"
        return redirect('/')
    else: 
        log = "logout"
    data ={
        'id': session['user_id']
    }
    return render_template('movie_add.html', user = User.get_by_id(data), log=log)

@app.route('/movies/<int:id>')
def view_movie(id):
    if 'user_id' not in session: 
        log = "login"
        return redirect('/')
    else: 
        log = "logout"
    data = {
        'id':session['user_id']
    }
    return render_template('movie_view.html', user=User.get_by_id(data), movie=Movie.get_by_id({'id':id}), log=log)

@app.route('/movies/edit/<int:id>')
def edit_user_profile(id):
    if 'user_id' not in session: 
        log = "login"
        return redirect('/')
    else: 
        log = "logout"
    user_data = {
        'id':session['user_id']
    }
    return render_template('movie_edit.html', user=User.get_by_id(user_data), movie=Movie.get_by_id({'id':id}), log=log)

@app.route('/movies/genre/<genre>')
def movies_by_genre(genre):
    if 'user_id' not in session: 
        log = "login"
        return redirect('/')
    else: 
        log = "logout"
    user_data = {
        'id':session['user_id']
    }
    return render_template('movies_genre.html', genre=genre, movies=Movie.get_by_genre(genre), user=User.get_by_id(user_data), log=log)

@app.route('/movies/year/<year>')
def movies_by_year(year):
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id':session['user_id']
    }
    return render_template('movies_year.html', year=year, movies=Movie.get_by_year(year), user=User.get_by_id(user_data))

#ACTIONS 
#ADD MOVIE
@app.route('/movies/add', methods=['POST'])
def add_movie():
    if 'user_id' not in session:
        return redirect('/')
    if not Movie.validate_movie(request.form):
        return redirect('/movies/submit')
    data = {
        "title": request.form['title'],
        "director": request.form['director'],
        "studio": request.form['studio'],
        "genre": request.form['genre'],
        "synopsis": request.form['synopsis'],
        "year": request.form['year']
    }
    Movie.save(data)
    return redirect('/movies')

#EDIT MOVIE
@app.route('/movies/edit_process/<int:id>', methods=['POST'])
def edit_movie(id):
    if 'user_id' not in session:
        return redirect('/')
    Movie.update_movie({'id':id})
    data = {
        'id': id, 
        'title': request.form['title'],
        "director": request.form['director'],
        "studio": request.form['studio'],
        "genre": request.form['genre'],
        "synopsis": request.form['synopsis'],
        "year": request.form['year']
    }
    Movie.update_movie(data)
    return redirect('/movies')

#DELETE MOVIE 
@app.route('/movies/eliminate/<int:id>')
def eliminate_movie(id):
    if 'user_id' not in session:
        return redirect('/')
    Movie.eliminate({'id':id})
    return redirect('/movies')

