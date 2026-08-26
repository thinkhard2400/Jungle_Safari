from datetime import datetime
from uuid import uuid4

import bcrypt
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from config import DATABASE_NAME, DEBUG, HOST, MONGO_URI, PORT


# 1. Flask와 MongoDB 준비
app = Flask(__name__)
CORS(app)  # 다른 포트에서 실행되는 프론트엔드의 요청을 허용합니다.

client = MongoClient(MONGO_URI)
database = client[DATABASE_NAME]

users = database["users"]
rooms = database["rooms"]


def error(message, code=400):
    """에러 메시지를 같은 형식으로 반환합니다."""
    return jsonify({"status": "error", "message": message}), code


def get_room(room_id):
    """방 ID로 MongoDB에서 방 하나를 찾습니다."""
    return rooms.find_one({"id": room_id}, {"_id": 0})


# 2. 서버가 정상적으로 실행되는지 확인하는 API
@app.route("/", methods=["GET"])
def home():
    return "Project 482 API is running!"


# 3. 회원가입 API
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}

    user_id = data.get("id", "")
    password = data.get("password", "")
    name = data.get("name", "")

    if not user_id or not password or not name:
        return error("id, password, name은 모두 필요합니다.")

    if users.find_one({"id": user_id}):
        return error("이미 존재하는 아이디입니다.", 409)

    # 비밀번호 원문 대신 암호화된 값을 저장합니다.
    encrypted_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    )

    users.insert_one({
        "id": user_id,
        "password": encrypted_password,
        "name": name,
    })

    return jsonify({
        "status": "success",
        "message": "회원가입이 완료되었습니다.",
    }), 201


# 4. 로그인 API
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    user_id = data.get("id", "")
    password = data.get("password", "")
    user = users.find_one({"id": user_id})

    if user is None:
        return error("아이디 또는 비밀번호가 잘못되었습니다.", 401)

    password_is_correct = bcrypt.checkpw(
        password.encode("utf-8"),
        user["password"],
    )

    if not password_is_correct:
        return error("아이디 또는 비밀번호가 잘못되었습니다.", 401)

    return jsonify({
        "status": "success",
        "message": "로그인 성공",
        "userId": user["id"],
        "name": user["name"],
    })


# 5. 운동방 목록 API
@app.route("/api/rooms", methods=["GET"])
def get_rooms():
    room_list = rooms.find({}, {"_id": 0}).sort("timestamp", -1)
    return jsonify({
        "status": "success",
        "rooms": list(room_list),
    })


# 6. 운동방 생성 API
@app.route("/api/rooms", methods=["POST"])
def create_room():
    data = request.get_json() or {}

    room_name = data.get("roomName", data.get("name", ""))
    host_id = data.get("hostId", "")
    host = users.find_one({"id": host_id})

    if not room_name or host is None:
        return error("방 이름과 유효한 hostId가 필요합니다.")

    room = {
        "id": uuid4().hex,
        "roomName": room_name,
        "time": data.get("time", ""),
        "maxMembers": int(data.get("maxMembers", 4)),
        "hostId": host_id,
        "status": "waiting",
        "timestamp": datetime.now().isoformat(),
        "members": [{
            "id": host_id,
            "name": host["name"],
            "isHost": True,
            "isReady": True,
            "logs": [],
        }],
    }

    rooms.insert_one(room)
    return jsonify({"status": "success", "room": room}), 201


# 7. 운동방 상세 조회 API
@app.route("/api/rooms/<room_id>", methods=["GET"])
def get_room_detail(room_id):
    room = get_room(room_id)

    if room is None:
        return error("방을 찾을 수 없습니다.", 404)

    return jsonify({"status": "success", "room": room})


# 8. 운동방 참여 API
@app.route("/api/rooms/<room_id>/join", methods=["POST"])
def join_room(room_id):
    data = request.get_json() or {}
    user_id = data.get("userId", "")
    room = get_room(room_id)
    user = users.find_one({"id": user_id})

    if room is None or user is None:
        return error("방 또는 사용자를 찾을 수 없습니다.", 404)

    for member in room["members"]:
        if member["id"] == user_id:
            return jsonify({"status": "success", "room": room})

    if len(room["members"]) >= room["maxMembers"]:
        return error("방 정원이 가득 찼습니다.", 409)

    rooms.update_one(
        {"id": room_id},
        {"$push": {"members": {
            "id": user_id,
            "name": user["name"],
            "isHost": False,
            "isReady": False,
            "logs": [],
        }}},
    )

    return jsonify({"status": "success", "room": get_room(room_id)})


# 9. 운동 시작, 일시정지, 종료 API
@app.route("/api/rooms/<room_id>/workout", methods=["POST"])
def workout(room_id):
    data = request.get_json() or {}
    user_id = data.get("userId", "")
    event_type = data.get("type", "")
    room = rooms.find_one({"id": room_id, "members.id": user_id})

    if room is None or event_type not in ["start", "pause", "stop"]:
        return error("room_id, userId, type을 확인해주세요.")

    event = {
        "type": event_type,
        "timestamp": datetime.now().isoformat(),
    }

    rooms.update_one(
        {"id": room_id, "members.id": user_id},
        {
            "$push": {"members.$.logs": event},
            "$set": {"status": event_type},
        },
    )

    return jsonify({
        "status": "success",
        "room": get_room(room_id),
    })


if __name__ == "__main__":
    app.run(debug=DEBUG, host=HOST, port=PORT)
