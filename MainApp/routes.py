# File to route the web app to appropriate address
from MainApp.functions.check_json import check_json
from MainApp import app
from flask import render_template

# Main route to check json request
@app.route('/check_json', methods=['POST'])
def postJsonHandler():
    msg = check_json()
    return msg

# Introduction/Default page if connect to server address, for example,  http://192.168.0.111:5000/
@app.route('/')
@app.route('/index')
def index():
    return render_template("base.html")
