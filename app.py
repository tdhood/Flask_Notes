"""Flask app for notes."""

from flask import Flask, request, jsonify
from models import db, connect_db, User

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

