# This file is used to run the Flask application in development mode.
from app.wsgi import app

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')