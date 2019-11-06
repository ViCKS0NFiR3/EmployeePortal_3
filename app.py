from flask import Flask
from datetime import timedelta, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/tura12$userdb'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'shhhh...iAmASecret!'