import uuid
from datetime import datetime
from flask import session
from flask_login import current_user
from db.models import DB, Users, Catalog


def set_language(request) -> dict:
    """Установка языка"""
    if not session.get('lng'):
        session['lng'] = 'eng'
    return session['lng']


def get_uniq() -> str:
    """Генерация уникального значения"""
    return str(uuid.uuid4())


def catalog_return(items: list) -> list:
    """Функция возвращения каталога"""
    return [{'id': item.id,
             'date': datetime.strftime(item.date, '%Y-%m-%d'),
             'type': item.type,
             'uniq': item.uniq,
             'name': item.name,
             'user_id': item.user_id,
             'level_0': item.level_0,
             } for item in items]
    
        
def get_users(id: int) -> list:
    """Получение пользователей"""
    if id == 0:
        items = DB.session.query(Users).all()
    else:
        items = DB.session.query(Users).filter_by(id=id).all()
    return [{'id': item.id,
             'username': item.username,
             'password': item.password,
             'language': item.language,
             } for item in items]


def get_documents_level_zero() -> list:
    """Получение документов level_0"""
    items = DB.session.query(Catalog).filter_by(user_id=current_user.id, level_0=True).order_by(Catalog.type, Catalog.date).all()
    return catalog_return(items)

    
def get_documents_by_uniq(uniq: str) -> list:
    """Получение документов по уникальному значению"""
    items = DB.session.query(Catalog).filter_by(user_id=current_user.id, uniq=uniq).order_by(Catalog.type, Catalog.date).all()
    return catalog_return(items)


