from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')

app.config.from_object('config')

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

app.config[
    "SQLALCHEMY_DATABASE_URI"] = f"mysql://{db_user}:{db_password}@localhost/{db_name}"
db = SQLAlchemy(app)
