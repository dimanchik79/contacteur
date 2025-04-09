from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class Users(UserMixin, DB.Model):
    """User Model"""
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(256), nullable=False)
    password = DB.Column(DB.String(162), nullable=False)
    
    def __repr__(self):
        return f"<User {self.username}>"
    
        
    
        
        