from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

from settings import setupConfig

app = Flask(__name__)
config = setupConfig(develop=True)
app.secret_key = 'Very secret key'
app.config.update(config)

db  = SQLAlchemy()
db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))

@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html', ctx={"name":session['user']})
    return redirect('/login')

@app.route('/login', methods=["GET", "POST"])
def login():
    if 'user' in session:
        return redirect('/')
    if request.method == 'POST':
        usr = User.query.filter_by(name=request.form['Username']).first()
        if request.form['Password'] == usr.password:
            session['user'] = usr.name
            return redirect('/')
    return render_template('login.html')

@app.route('/adduser', methods=['POST'])
def adduser():
    usr = User(name=request.form['Username'], password=request.form['Password'])
    print(usr)
    db.session.add(usr)
    db.session.commit()
    return redirect('/')

@app.route('/removeuser', methods=['POST'])
def removeuser():
    usr = User.query.filter_by(name=request.form['Username']).first()
    db.session.delete(usr)
    db.session.commit()
    return redirect('/')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == "__main__":
   app.run()