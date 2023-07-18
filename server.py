from flask import render_template, session, redirect, request
from movies_app import app
from movies_app.controllers import users, movies


if __name__ == "__main__":
    app.run(debug=True, port=5001)