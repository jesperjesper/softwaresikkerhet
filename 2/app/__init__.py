

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#oppgave3
from flask_login import UserMixin, LoginManager, current_user
#limiter

import os
import pyotp


app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import routes

from .models import User
#login prøver


login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

