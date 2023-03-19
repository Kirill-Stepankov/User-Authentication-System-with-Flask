from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
login = LoginManager(app)
mail = Mail(app)

from app.authentication import bp as auth_bp
app.register_blueprint(auth_bp)

from app.main import bp as main_bp
app.register_blueprint(main_bp)

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)


login.login_view = 'auth.login'

from app import models


@login.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)
