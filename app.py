# Main file to run the web app
# Must import necessary components from MainApp package to run
from MainApp import app, routes

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
