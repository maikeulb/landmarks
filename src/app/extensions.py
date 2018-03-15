from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

migrate = Migrate()
db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)
