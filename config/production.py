from config.default import *
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv(os.path.join(BASE_DIR, '.env'))

# 데이터베이스 URI 설정
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8'

# 시크릿 키 설정
SECRET_KEY = os.getenv('SECRET_KEY')

# JWT 시크릿 키 설정
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
