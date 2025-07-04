from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, NoteForm
from models import db, User
import requests
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://web_app_user:DSimH1jlnDU6QOtx5d4cbyf4U3tKe7SH@dpg-d1dd2ap5pdvs73am2cng-a/web_app_db_c1ry'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = NoteForm(notes=current_user.notes)
    if form.validate_on_submit():
        current_user.notes = form.notes.data
        db.session.commit()
    crypto_data = get_crypto_data()
    return render_template('dashboard.html', form=form, notes=current_user.notes or '', crypto=crypto_data)


@app.route('/delete_notes')
@login_required
def delete_notes():
    current_user.notes = ''
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


def get_crypto_data():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd')
        data = response.json()
        if 'bitcoin' in data and 'ethereum' in data:
            return data
        else:
            return {'error': 'Brakuje danych dla bitcoin lub ethereum'}
    except:
        return {'error': 'Nie udało się pobrać danych z API'}


if __name__ == '__main__':
    app.run(debug=True)
