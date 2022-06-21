"""Flask app for notes."""

from flask import Flask, request, jsonify, redirect, render_template, flash
from models import db, connect_db, User
from forms import AddUserForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notebooks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

# User Routes 
########################################################################

@app.get("/")
def root():
    """Render register page"""

    return redirect('/register')

@app.route("/register", methods=["GET", "POST"])
def show_form_and_handle_create_user():
    """Load form; handle creating user"""

    form = AddUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name)

        db.session.add(user)
        db.session.commit()

        return redirect('/secret')
