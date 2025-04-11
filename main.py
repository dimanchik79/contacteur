import os
from flask import Flask, redirect, url_for
from dotenv import load_dotenv
from flask_wtf import CSRFProtect
from flask_login import LoginManager

from db.models import DB, Users

from routes.users import users
from routes.contacter import contacteur


app = Flask(__name__)

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(contacteur)

load_dotenv()
app.config['SESION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SECRET_KEY'] = os.getenv('secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db')
app.app_context().push()
DB.init_app(app)


login_manager = LoginManager(app)
login_manager.login_view = 'users.authorize'
csrf = CSRFProtect(app)


@login_manager.user_loader
def load_user(user_id) -> object:
    """Загрузка пользователя"""
    try:
        return DB.session.query(Users).filter_by(id=user_id).one()
    except Exception:
        return redirect(url_for('users.authorize'))
        
        
def main():
    DB.create_all()
    app.run(host='0.0.0.0', port='5002', debug=True)
    

if __name__ == "__main__":
    main()
