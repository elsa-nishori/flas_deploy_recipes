from flask import redirect, render_template, request, session
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def log_and_reg():
    return render_template("log_and_reg.html")

@app.route('/register', methods=["POST"])
def register():
    if not User.validate_user_reg(request.form):
        return redirect('/')
    
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    reg_data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": hashed_pw
    }

    user_id = User.register(reg_data)
    session['user_id'] = user_id
    return redirect('/recipes')

@app.route('/login', methods=["POST"])
def login():
    if not User.validate_user_log(request.form):
        return redirect('/')
    user = User.get_user_by_email(request.form)
    session['user_id'] = user.id
    return redirect('/recipes')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


