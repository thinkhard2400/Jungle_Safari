import os
from dotenv import load_dotenv

load_dotenv()

# 민감한 값은 서버 환경변수에서 읽고, 로컬에서는 기본값을 사용합니다.
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "project_482")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "assign_secret_key")
TW_SID = os.getenv("TW_SID")
TW_AUTH = os.getenv("TW_AUTH")
TW_SENDER = os.getenv("TW_SENDER")
# Flask 서버 설정
DEBUG = False
HOST = "0.0.0.0"
PORT = 5000

# Flask 로컬 설정 
# DEBUG = True
# HOST = "127.0.0.1"
# PORT = 5001
