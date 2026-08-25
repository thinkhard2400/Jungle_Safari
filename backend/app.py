from flask import Flask, jsonify, request
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

# MongoDB Atlas 연결 설정
MONGO_URI = "mongodb+srv://thinkhard2400_db_user:8YQDMjpal5Ncau0w@safaricluster.nclev4w.mongodb.net/?retryWrites=true&w=majority&appName=SafariCluster"

client = MongoClient(MONGO_URI)
db = client["project_482"]
users_collection = db["users"]

@app.route('/')
def index():
    return jsonify({"message": "Project 482 Backend API with MongoDB Atlas"})

@app.route('/test-db')
def test_db():
    try:
        db.command("ping")
        return jsonify({"status": "success", "message": "MongoDB Atlas connected successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# 회원가입 API
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user_id = data.get('id')
    password = data.get('password')
    name = data.get('name')

    if not user_id or not password or not name:
        return jsonify({"status": "fail", "message": "모든 필드를 입력해주세요."}), 400

    if users_collection.find_one({"id": user_id}):
        return jsonify({"status": "fail", "message": "이미 존재하는 아이디입니다."}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    users_collection.insert_one({
        "id": user_id,
        "password": hashed_password,
        "name": name
    })

    return jsonify({"status": "success", "message": "회원가입이 완료되었습니다."})

# 로그인 API
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data.get('id')
    password = data.get('password')

    if not user_id or not password:
        return jsonify({"status": "fail", "message": "아이디와 비밀번호를 입력해주세요."}), 400

    user = users_collection.find_one({"id": user_id})

    if not user:
        return jsonify({"status": "fail", "message": "존재하지 않는 아이디입니다."}), 400

    if bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({"status": "success", "message": "로그인 성공", "name": user['name']})
    else:
        return jsonify({"status": "fail", "message": "비밀번호가 일치하지 않습니다."}), 400

if __name__ == '__main__':
    app.run(debug=True)