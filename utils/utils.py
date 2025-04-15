import uuid
from flask import session
from db.models import DB, Users


def set_language(request) -> dict:
    """Установка языка"""
    if not session.get('lng'):
        session['lng'] = 'eng'
    return session['lng']


def get_uniq() -> str:
    """Генерация уникального значения"""
    return str(uuid.uuid4())
    
        
def get_users(id: int) -> list:
    if id == 0:
        items = DB.session.query(Users).all()
    else:
        items = DB.session.query(Users).filter_by(id=id).all()
    return [{'id': item.id,
             'username': item.username,
             'password': item.password,
             'language': item.language,
             } for item in items]

