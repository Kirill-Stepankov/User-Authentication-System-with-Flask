from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_babel import Babel
from authlib.integrations.flask_client import OAuth


app = Flask(__name__)
app.config.from_object(Config)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
login = LoginManager(app)
mail = Mail(app)
babel = Babel(app)
oauth = OAuth(app)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

oauth.register(
    name='github',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

def get_locale():
    if current_user.is_anonymous:
        return request.accept_languages.best_match(app.config['LANGUAGES'])
    return current_user.language


babel.init_app(app, locale_selector=get_locale)

from app.authentication import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from app.oauth import bp as oauth_bp
app.register_blueprint(oauth_bp, url_prefix='/oauth')

from app.main import bp as main_bp
app.register_blueprint(main_bp)

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

login.login_view = 'auth.login'

from app import models


@login.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)
