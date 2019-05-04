from flask import Flask

from db import db
from ma import ma

app = Flask(__name__)

app.secret_key = 'secret'
app.config['SECRET_KEY'] = 'secret!'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.before_first_request
def create_tables():
    db.create_all()

from vievs.viev import *

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(debug=True, host='localhost', port=5000)

