# -*- coding: utf-8 -*-
from flask import Flask
from flask import  render_template , request , redirect , url_for ,flash , session
from flask.ext import sqlalchemy
from config import DATABASE ,SECRET_KEY
import re
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SECRET_KEY'] = SECRET_KEY

# database
db = sqlalchemy.SQLAlchemy(app)

class user(db.Model):
    UID = db.Column(db.Integer , primary_key=True,autoincrement=True,unique=True) #id
    Username = db.Column(db.String )
    Password = db.Column(db.String )
    Email = db.Column(db.String )
    School = db.Column(db.String , nullable = True)
    Age = db.Column(db.Integer)
    Blog = db.Column(db.String)
    Introduction = db.Column(db.String)

    def __init__(self , username , password , email , school = 'none' , age = 0 , blog='http://baidu.com',introdution='i am too lazy~~'):
        self.Username = username
        self.Password = password
        self.Email = email
        self.School = school
        self.Age = age
        self.Blog = blog
        self.Introduction =introdution
    def __repr__(self):
        return '<User %s>'%self.Username

def vali(newone):
    if len(newone.Password) < 6:
        return 0
    return 1
# views
@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/reg',methods=['GET','POST'])
def reg():
    if request.method == 'GET':
        print "get"
        return render_template('reg.html')
    else:
        print "post"
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repassword']
        email = request.form['email']

        print "< %s %s %s>" % (username , password ,email)
        if password != repassword:
            flash("passwords doesn't match!!")
            return render_template('reg.html')

        newuser = user(username , password , email )
        print newuser
        if vali(newuser):
            db.session.add(newuser)
            db.session.commit()
            flash("Registration is successful!")
            return redirect(url_for('info'))
        else :
            flash("Registration is not successful!")
            return redirect(url_for('login'))

@app.route('/login' , methods=['GET','POST'])
def login():
    print 'into log view'
    if 'username' in session:
        print "logged"
        flash("Already logged in, please exit!")
        return redirect(url_for('info'))
    else :
        print 'nologged'
        if request.method == 'GET':
            return render_template('login.html')
        else :
            email = request.form['email']
            password = request.form['password']
            User = user.query.filter_by(Email = email , Password = password).first()
            if User is None:
                flash("email or password is wrong!!")
                return render_template('login.html')
            else:
                session['username'] = User.Username
                session['email'] = User.Email
                flash("login successful!")
                return render_template('info.html',user = User)

@app.route('/logout')
def logout():
    if 'username' in session:
        session.clear()
        return render_template('sucexit.html')
    else:
        return render_template('nologin.html')

@app.route('/info')
def info():
    if 'username' in session:
        User = user.query.filter_by(Email = session['email']).first()
        return render_template('info.html',user =User)
    else :
        flash("Please login system first !!")
        return redirect(url_for('login'))


@app.route('/edit' , methods=['GET','POST'])
def editinfo():

    if 'username' in session:

        User = user.query.filter_by(Email = session['email']).first_or_404()
        if request.method == 'POST':
            if request.form['username'] != "":
                print request.form['username']
                User.Username = request.form['username']
            if request.form['school'] != "":
                print request.form['school']
                User.School = request.form['school']
            if request.form['blog'] != "":
                print request.form['blog']
                User.Blog = request.form['blog']
            if request.form['intro'] != "":
                print request.form['intro']
                User.Introduction = request.form['intro']
            if request.form['age'] != "":
                print  request.form['age']
                User.Age =int( request.form['age'] )
            db.session.commit()
            return redirect(url_for('info'))
        else :
            return render_template('edit.html',user =User)
    else :
        flash("Please login system first !!")
        return redirect(url_for('login'))
@app.route('/changepassword',methods=['GET','POST'])
def changepassword():
    if 'username' in session:
        if request.method == 'GET':
            return render_template('changepassword.html')
        else:
            password = request.form['password']
            newpassword = request.form['password']
            repassword = request.form['password']
            if user.query.filter_by(Email=session['email']).first().Password != password or newpassword != repassword or len(newpassword) < 6:
                flash("password is wrong , or newpassword isn't match!")
                return render_template('changepassword.html')
            else:
                user.query.filter_by(Email=session['email']).first().Password = newpassword
                db.session.commit()
                flash("Changed password!!")
                return redirect(url_for('info'))
    else:
        flash("Please login system first !!")
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
