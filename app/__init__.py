from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import redis
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# 데이터베이스 객체가 생성될 때 이 네이밍 규칙이 적용됨
# 테이블, 제약 조건 등을 생성할 때 개발자가 일일이 이름을 정의할 필요가 없어짐
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
redis_host = os.getenv('REDIS_HOST') or 'localhost'
jwt_redis = redis.StrictRedis(host=redis_host, port=6379, db=0)


class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_SUPPORTS_CREDENTIALS = True
    JWT_DECODE_ALGORITHMS = ['HS256']
    JWT_TOKEN_LOCATION = ['headers']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=14)
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_METHODS = ['POST', 'PUT', 'PATCH', 'DELETE']
    JWT_CSRF_CHECK_FORM = True
    JWT_CSRF_IN_COOKIES = True


def create_app():
    app = Flask(__name__)

    # Config 클래스 사용
    app.config.from_object(Config)
    app.config.from_envvar('APP_CONFIG_FILE', silent=True)

    # CORS(app, resources={r'*': {'origins': 'http://10.0.0.4'}})
    CORS(app)
    
    # 여기에 db.init_app(app) 추가
    db.init_app(app)
    
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Blueprints
    from .api import posts, members
    app.register_blueprint(posts.bp)
    app.register_blueprint(members.bp)

    return app