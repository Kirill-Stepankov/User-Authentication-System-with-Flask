from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.authentication import handlers, forms, email
