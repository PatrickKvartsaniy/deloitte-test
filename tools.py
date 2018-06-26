import json

from functools import wraps

from flask import session,redirect

def setupConfig(develop=False, prod=False):
    #This func take config from config.json and add them to the application
    try:
        with open("config.json", 'r') as c:
            conf = json.load(c)
            if develop:
                return conf['DEVELOP']
            return conf['PROD']
    except Exception as e:
        print(f"Setup config error: {e}")

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/login')
    return wrap
		