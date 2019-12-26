from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '229b845d2e364ca8a032e35c104f69b1'
app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite:///video.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

from videorentalstore import routes