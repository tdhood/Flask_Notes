"""Flask app for notes."""

from flask import Flask, request, jsonify, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import AddUserForm, LoginUserForm, CSRFProtectForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///notebooks"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

app.config["SECRET_KEY"] = "oh-so-secret"
debug = DebugToolbarExtension(app)

connect_db(app)

db.create_all()


# User Routes
########################################################################


@app.get("/")
def root():
    """Render register page"""

    return redirect("/register")


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

        user = User.register(username, password, email, first_name, last_name)

        db.session.add(user)
        db.session.commit()

        return redirect("/users/<username>")
    else:
        return render_template("user_register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def show_login_form_and_authenticate_user():
    """load login form and authenticate user"""

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("user_login.html", form=form)


@app.get("/users/<username>")
def show_secret(username):
    """show secret"""

    user = User.query.get_or_404(username)
    form = CSRFProtectForm()

    return render_template("secret.html", form=form)


@app.post("/logout")
def logout():
    """logs user out and redirects to homepage"""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("username", None)

    return redirect("/")
