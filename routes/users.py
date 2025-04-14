from flask import Blueprint, redirect,render_template, request, url_for, session
from flask_login import login_required, login_user, logout_user, current_user

from werkzeug.security import check_password_hash

from db.models import DB, Users
from utils.utils import get_users, set_language
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
    lng = set_language(request)
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
    return render_template("users/authorize.html",
                           error=err,
                           title=LANG['auth_title'][lng],
                           language=LANG,
                           lang_list=lang_list,
                           _lng=lng)


@users.route('/registration', methods=['GET', 'POST'])
def registration() -> render_template:
    """Заявка на регистрацию пользователя"""
    err = ""
    lng = set_language(request)
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
                                password=password,
                                language=lng)
                DB.session.add(registr)
                DB.session.commit()
                return redirect(url_for('.authorize'))
    return render_template('users/registration.html', 
                           error=err,
                           title=LANG['registration_title'][lng],
                           language=LANG,
                           lang_list=lang_list,
                           _lng=lng)


@users.route('/change_lang/<lng>', methods=['GET', 'POST'])
def change_lang(lng) -> redirect:
    """Смена языка сайта"""
    if lng in ['ru', 'en']:
        session['lng'] = lng
    return redirect(url_for('.authorize'))
    
