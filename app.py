"""Flask app for notes."""

from flask import Flask, request, jsonify, redirect, render_template, flash
from models import db, connect_db, User
from forms import AddUserForm, LoginUserForm

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

        user = User.register(username, password, email,
                            first_name, last_name)

        db.session.add(user)
        db.session.commit()

        return redirect('/secret')

@app.route("/login", methods=["GET","POST"])
def show_login_form_and_authenticate_user():
    """load login form and authenticate user"""

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect("/secret")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("user_login.html", form=form)

@app.route("/secret", methods="GET")
def show_secret():
    """show secret"""
    form = ShowSecret()

    return render_template("secret.html")
