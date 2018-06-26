import os
import json

from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

from tools import setupConfig, login_required

app = Flask(__name__)
config = setupConfig(prod=True)
app.secret_key = 'Very secret key'
app.config.update(config)

db  = SQLAlchemy()
db.init_app(app)

# User model for postgres
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))

@app.route('/')
@login_required
def index():
    return render_template('index.html', ctx={"name":session['user'],"resut":""})

@app.route('/login', methods=["GET", "POST"])
def login():
    if 'user' in session:
        return redirect('/')
    if request.method == 'POST':
        try:
            usr = User.query.filter_by(name=request.form['Username']).first()
            if request.form['Password'] == usr.password:
                session['user'] = usr.name
                return redirect('/')
            else:
                return render_template('login.html',ctx="Password is wrong or user does not exist")
        except AttributeError:
            return render_template('login.html',ctx="User does not exist")
    return render_template('login.html', ctx="")

@app.route('/adduser', methods=['POST'])
@login_required
def adduser():
    usr = User.query.filter_by(name=request.form['Username']).first()
    if usr:
        return render_template('index.html', ctx={"name":session['user'], "result":"User already registred"})
    else:
        usr = User(name=request.form['Username'], password=request.form['Password'])
        db.session.add(usr)
        db.session.commit()
        return render_template('index.html', ctx={"name":session['user'], "result":"Success"})

@app.route('/removeuser', methods=['POST'])
@login_required
def removeuser():
    usr = User.query.filter_by(name=request.form['Username']).first()
    if usr:
        usr = User.query.filter_by(name=request.form['Username']).first()
        db.session.delete(usr)
        db.session.commit()
        return render_template('index.html', ctx={"name":session['user'], "result":"Success"})
    else:
        return render_template('index.html', ctx={"name":session['user'], "result":"User does not exist"})

@app.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == "__main__":
    host, port = '0.0.0.0', int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)