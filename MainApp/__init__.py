# Initial file contain setup for the MainApp package
from flask import Flask
from MainApp.config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from MainApp import models
