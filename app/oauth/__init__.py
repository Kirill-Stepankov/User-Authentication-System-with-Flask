from flask import Blueprint

bp = Blueprint('oauth', 'auth')

from app.oauth import handlers