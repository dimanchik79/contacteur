from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class Users(UserMixin, DB.Model):
    """User Model"""
    id = DB.Column(DB.Integer, primary_key=True, )
    username = DB.Column(DB.String(256), nullable=False)
    password = DB.Column(DB.String(162), nullable=False)
    language = DB.Column(DB.String(3), nullable=False, default='eng')
    
    catalog = DB.relationship('Catalog', backref='users')
    
    def __repr__(self):
        return f"<User {self.username}>"
    
class Catalog(DB.Model):
    """Catalog Model"""
    id = DB.Column(DB.Integer, primary_key=True)
    date = DB.Column(DB.DateTime, nullable=False, default=datetime.utcnow())
    uniq = DB.Column(DB.String(36), nullable=False)
    type = DB.Column(DB.Integer, nullable=False)
    name = DB.Column(DB.String(256), nullable=False)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'), nullable=False)  
    
    
    
        
    
        
        