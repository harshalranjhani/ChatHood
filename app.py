from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from db import get_user, save_user
from pymongo.errors import DuplicateKeyError

app = Flask(__name__)
app.secret_key = 'qyvcuyw39994uibfd'
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/login",methods=["GET","POST"])
def login():
    message = ""

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')
        user = get_user(username)

        if user and user.check_password(password_input):
            login_user(user)
            return redirect(url_for('home'))
        else:
            message = "Username or password is incorrect!"
            return render_template('login.html',message=message)
    return render_template('login.html')


@app.route('/signup',methods=["GET","POST"])
def signup():
    message = ""
    if current_user.is_authenticated:
        message = "Already logged in!"
        return url_for('home')

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password_input = request.form.get('password')
        try:
            save_user(username, email, password_input)
            return redirect(url_for('login'))
        except DuplicateKeyError:
            message = "User already exists"
            return render_template('signup.html',message=message)
    return render_template('signup.html')


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/chat')
@login_required
def chat():
    return render_template('select.html')

@app.route('/chat/friends')
def friends_chat():
    return render_template('chat.html')

@login_manager.user_loader
def load_user(username):
    return get_user(username)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
