import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')

app.config.from_object('config')

login_manager = LoginManager(app)

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

app.config[
    "SQLALCHEMY_DATABASE_URI"] = f"mysql://{db_user}:{db_password}@localhost/{db_name}"
app.config['SECRET_KEY'] = 'change-this-secret-key'
db = SQLAlchemy(app)
app.jinja_env.globals['now'] = datetime.now

with app.app_context():
    db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'
