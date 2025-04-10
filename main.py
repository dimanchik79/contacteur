import os
from flask import Flask, redirect, url_for
from dotenv import load_dotenv
from flask_wtf import CSRFProtect
from flask_login import LoginManager

from db.models import DB

from routes.users import usersblock


app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db')
app.app_context().push()
DB.init_app(app)


login_manager = LoginManager(app)
login_manager.login_view = 'usersblock.authorize'
csrf = CSRFProtect(app)


@login_manager.user_loader
def load_user(user_id) -> object:
    """Загрузка пользователя"""
    try:
        return
        # return DB.session.query(Users).filter_by(id=user_id).one()
    except Exception:
        return
        # return redirect(url_for('usersblock.authorize'))
        
        
def main():
    # DB.create_all()
    app.run(host='0.0.0.0', port='5002', debug=True)
    

if __name__ == "__main__":
    main()
