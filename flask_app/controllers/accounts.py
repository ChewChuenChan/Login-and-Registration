from flask_app import app
from flask_bcrypt import Bcrypt
from flask import render_template,request,redirect,session,flash
from flask_app.models.account import Account
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=["POST"])
def register():
    if not Account.validate_register(request.form):
        return redirect('/')
    data ={
        "first_name" :request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : bcrypt.generate_password_hash(request.form["password"])
        }
    account_id = Account.create(data)
    session['account_id'] = account_id
    return redirect('/dashboard')


@app.route('/login',methods=["POST"])
def login():
    this_account = Account.get_by_email({"email" : request.form["email"]})
    if this_account and bcrypt.check_password_hash(this_account.password,request.form['password']):
        session['account_id'] = this_account.id
        return redirect('/dashboard') 
    flash("Invalid Email/Password","login")
    return redirect ('/')

@app.route('/dashboard')
def dashboard():
    if 'account_id' not in session:
        return redirect ('/logout')
    data = {
        'id': session['account_id']
    }
    one_account = Account.get_by_id(data)
    return render_template("dashboard.html",one_account = one_account)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')