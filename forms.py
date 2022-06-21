"Forms for Notes app"
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Email

class AddUserForm(FlaskForm):
    """form for adding Users"""

    username = StringField("Username", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])