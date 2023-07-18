from movies_app import app
from flask import Flask, redirect, render_template, request, flash, session 
from ..models.user import User
from ..models.movie import Movie
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
dateFormat = "%#m/%#d/%Y %I: %M %p"

@app.route('/')
def login_and_reg():
    return render_template("user_login_and_reg.html")

@app.route('/users')
def all_users():
    if 'user_id' not in session: 
        log = "login"
        return redirect('/')
    else: 
        log = "logout"
    data ={
        'id': session['user_id']
    }
    return render_template('users_all.html', users=User.get_all(), user=User.get_by_id(data), log=log)

@app.route('/users/<int:id>')
def show_user(id):
    if 'user_id' not in session: 
        log = "login"
        return redirect('/')
    else: 
        log = "logout"
    session_data ={
        'id': session['user_id']
    }
    data = {
        "id": id
    }
    return render_template('user_profile.html', active_user=User.get_by_id(session_data), user=User.get_by_id(data), log=log)

@app.route('/user_likes/<int:id>')
def user_liked_films(id):
    if 'user_id' not in session: 
        log = "login"
        return redirect('/')
    else: 
        log = "logout"
    data ={
        "id": id
    }
    return render_template('user_likes.html', user=User.get_by_id(data), log=log)

#ACTIONS/POSTS
@app.route("/register", methods=['POST'])
def reg():

    if not User.validate_reg(request.form):
        return redirect('/')
    data = {
        "user_name": request.form['user_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.register_user(data)
    session['user_id'] = id 
            
    return redirect('/movies')

@app.route('/login', methods=['POST'])
def login_user():
    user = User.get_email(request.form)

    if not user: 
        flash("Incorrect email", "login_error")
        return redirect('/')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Incorrect password", "login_error")
        return redirect('/')

    session['user_id'] = user.id

    return redirect('/movies')

@app.route('/users/edit/<int:id>')
def edit_page(id):
    if 'user_id' not in session: 
        log = "login"
        return redirect('/')
    else: 
        log = "logout"
    session_data ={
        'id': session['user_id']
    }
    return render_template('user_edit.html', user=User.get_by_id({'id':id}), log=log)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# EDIT USER PROFILE
@app.route('/users/edit_process/<int:id>', methods=['POST'])
def edit_user(id):
    if 'user_id' not in session:
        return redirect('/')
    User.update_user({'id':id})
    data = {
        'id': id,
        'real_name': request.form['real_name'],
        'gender': request.form['gender'],
        'bio': request.form['bio']
    }
    User.update_user(data)
    return redirect('/users')

@app.route('/like/movie', methods=['POST'])
def like_movie():
    data = {
        'movie_id': request.form['movie_id'],
        'user_id': request.form['user_id']
    }
    User.add_like(data)
    return redirect("/movies")

@app.route('/movies/add_favorite', methods=['POST'])
def liked_movie():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'movie_id': request.form['movie_id'],
        'user_id': session['user_id']
    }
    User.add_like(data)
    return redirect('/movies')