from flask import Flask
from flask import request
from flask import abort
from functools import wraps
from hashlib import sha256
from datetime import datetime

app = Flask(__name__)

def get_date_string():
    date = datetime.now()
    date_string = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
    return date_string

def authorize(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        hashed_authorization = request.headers.get('Authorization')
        date = get_date_string()
        secret = 'Matt'
        date_secret = secret + date
        hashed_secret = sha256(date_secret.encode('utf-8')).hexdigest()
        if hashed_authorization != hashed_secret:
            abort(401)
        return func(*args, **kwargs)
    return decorated_function

@app.route('/')
@authorize
def hello():
    return "Hello World"

@app.route('/isAlive')
def index():
    return "true"
   
if __name__ == '__main__':
    app.run()        
    # app.run(debug=True)