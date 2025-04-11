from flask import Blueprint, redirect,render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from werkzeug.security import check_password_hash

from db.models import DB, Users
from utils.utils import get_users
from utils.lang import lang_list, lang as LANG

users = Blueprint('users', __name__)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.authorize'))


@users.route('/authorize', methods=['GET', 'POST'])
def authorize() -> render_template:
    """Авторизация пользоваетеля"""
    title = LANG['auth_title']['en']
    err = ""
    if request.method == 'POST':
        user = Users.query.filter_by(username=request.form['username']).first()
        if user:
            if user.username == request.form['username'] and check_password_hash(user.password, request.form['password']):
                login_user(user, remember=True)
                return redirect(url_for('contacteur.index'))
            else:
                err = "Неверный пароль"
        else:
            err = "Такой пользователь не существует"
    return render_template("users/authorize.html", err=err, title=title)


@users.route('/registration', methods=['GET', 'POST'])
def registration() -> render_template:
    """Заявка на регистрацию пользователя"""
    err = ""
    if request.method == 'POST':
        if 'cancel' in request.form:
            return redirect(url_for('.authorize'))
        
        if 'register' in request.form:
            username = request.form['username']
            password = request.form['password']
            if username == "" and password == "":
                    err = "Все поля должны быть заполненны"
            conn = DB.session.query(Users).filter_by(username=request.form['username']).first()
            if conn:
                err = "Пользователь с таким логином уже существует"
        if err == "":
                registr = Users(username=username, 
                                password=password)
                DB.session.add(registr)
                DB.session.commit()
                return redirect(url_for('.authorize'))
    return render_template('users/registration.html', err=err)
