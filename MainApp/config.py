# Configuration file for the MainApp package
# Containing configuration for database and the web app
class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@localhost:3306/customer_DB'
    SECRET_KEY = "youcanguessbutitisimpossible"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
