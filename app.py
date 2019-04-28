from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
db = SQLAlchemy()
ma = Marshmallow()

app.config['SECRET_KEY'] = 'secret!'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html',
                           welcome_message="Witamy na platformie egzaminacyjnej",
                           is_login=False,
                           username='Krystyna'
                           )


if __name__ == '__main__':
    db.init_app(app)
    app.run(host='localhost', port=5000)

