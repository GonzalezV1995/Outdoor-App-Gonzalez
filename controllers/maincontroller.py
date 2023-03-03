from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt

from flask_app.models.user import User

bcrypt = Bcrypt(app)


@app.route('/')  
def dashboard():
    return render_template('dashboard.html')  # first page user sees and once any button is clicked it redirects you to log in and register(index.html)


@app.route('/index')
def index():
    return render_template('index.html') #this is the log in and register page 


# registration 
@app.route('/register', methods=['POST'])
def register():
    
    if not User.validate_registration(request.form):
        return redirect('/index') 

    User.save( 
        {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password']),
        'city' : request.form['city'],
        'state' : request.form['state'],
    }
    )
    user = User.get_email(
        {
            'email': request.form['email']
        }
    )
    session['user_id'] = user.id

    return redirect('/userdashboard')


#log in 
@app.route('/user/login', methods=['POST'])
def login():
    
    user = User.get_email(
        {'email': request.form['email']}
    )

    if not user or not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Credentials", "login")
        return redirect('/index')
    
    session['user_id'] = user.id
    # has to do credential check before using session key note!
    return redirect('/userdashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')