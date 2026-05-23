# models/__init__.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .post import Post

__all__ = ['db', 'User', 'Post']
