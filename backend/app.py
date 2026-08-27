from datetime import datetime, timedelta, timezone
from uuid import uuid4

import bcrypt
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from pymongo import MongoClient
from config import DATABASE_NAME, DEBUG, HOST, JWT_SECRET_KEY, MONGO_URI, PORT, TW_AUTH, TW_SID, TW_SENDER
from flask_jwt_extended import *
from routes.page import page_bp

from twilio.rest import Client as TwilioClient

# 1. Flask와 MongoDB 준비
app = Flask(
    __name__,
    static_folder="../frontend",
    template_folder="../frontend",
    static_url_path="",
)
CORS(app)  # 다른 포트에서 실행되는 프론트엔드의 요청을 허용합니다.
app.register_blueprint(page_bp)
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
# API 테스트 단계에서는 쿠키의 CSRF 헤더 검사를 끕니다.
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token_cookie"
app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token_cookie"


twclient = TwilioClient(TW_SID,TW_AUTH)
client = MongoClient(MONGO_URI)
database = client[DATABASE_NAME]
jwt = JWTManager(app) ## jwt manager 가 secret key 를 관리 

users = database["users"]
rooms = database["rooms"]


def error(message, code=400):
    """에러 메시지를 같은 형식으로 반환합니다."""
    return jsonify({"status": "error", "message": message}), code


def get_room(room_id):
    """방 ID로 MongoDB에서 방 하나를 찾습니다."""
    return rooms.find_one({"id": room_id}, {"_id": 0})

def send_sms(receiver, name):
    return twclient.messages.create(
        to=receiver,
        from_=TW_SENDER,
        body= f"{name}님 곧 운동이 시작됩니다!",
    )



### API Route

# 2. 서버가 정상적으로 실행되는지 확인하는 API
@app.route("/api/health", methods=["GET"])
def health():
    return "Project 482 API is running!"


# 3. 회원가입 API
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}

    user_id = data.get("id", "")
    password = data.get("password", "")
    name = data.get("name", "")
    phone = data.get("phone", "")

    if not user_id or not password or not name or not phone:
        return error("id, password, name, phone은 모두 필요합니다.")

    if users.find_one({"id": user_id}):
        return error("이미 존재하는 아이디입니다.", 409)

    # 비밀번호 평문 대신 해시값을 저장.
    encrypted_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    )
    parsed_phone =  "+82" + phone.replace("-", "")[1 :]
    users.insert_one({
        "id": user_id,
        "password": encrypted_password,
        "name": name,
        "phone" : parsed_phone
    })

    return jsonify({
        "status": "success",
        "message": "회원가입이 완료되었습니다.",
    }), 201


# 3. 로그인 API
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

    if password_is_correct:
         # assign access & refresh token 
        access_token = create_access_token(
            identity=user_id,
            expires_delta=timedelta(minutes=60),

        )
        refresh_token = create_refresh_token(
            identity=user_id,
            expires_delta=timedelta(days=14),
        )
        response = jsonify({"result": "success", "message": "로그인 성공", "userId": user["id"],"name": user['name']})
        response.set_cookie("access_token_cookie", access_token, max_age=3600, path="/", secure=False, httponly=True, samesite="Lax")
        response.set_cookie("refresh_token_cookie", refresh_token, max_age=604800, path="/", secure=False, httponly=True, samesite="Lax")
        
        return response
    else : 
        return jsonify({"result": "fail", "message": "비밀번호가 일치하지 않습니다."}), 400

    
       
    
        

    


# 4. 운동방 목록 API
@app.route("/api/rooms", methods=["GET"])
def get_rooms():
    room_list = rooms.find({}, {"_id": 0}).sort("timestamp", -1)
    room_data = []

    for room in room_list:
        room_data.append({
            "id": room["id"],
            "type": room.get("type", "런닝"),
            "time": room.get("time", ""),
            "name": room.get("name", room.get("roomName", "")),
            "max": room.get("max", room.get("maxMembers", 4)),
            "status": room.get("status", "waiting"),
            "timestamp": room.get("timestamp"),
            "members": room.get("members", []),
        })

    return jsonify({"rooms": room_data})


# 5. 운동방 생성 API
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
        "type": data.get("type", "런닝"),
        "name": room_name,
        "time": data.get("time", ""),
        "max": int(data.get("max", data.get("maxMembers", 4))),
        "hostId": host_id,
        "status": "waiting",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "members": [{
            "id": host_id,
            "name": host["name"],
            "isHost": True,
            "isReady": True,
            "logs": [],
        }],
    }

    rooms.insert_one(room)
    return jsonify({"status": "success", "room": get_room(room["id"])}), 201


# 6. 운동방 상세 조회 API
@app.route("/api/rooms/<room_id>", methods=["GET"])
def get_room_detail(room_id):
    room = get_room(room_id)

    if room is None:
        return error("방을 찾을 수 없습니다.", 404)

    return jsonify({"status": "success", "room": room})


# 7. 운동방 참여 API
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

    max_members = room.get("max", room.get("maxMembers", 4))

    if len(room["members"]) >= max_members:
        return error("방 정원이 가득 찼습니다.", 409)

    # waiting 상태 일때만 추가 
    result = rooms.update_one(
        {"id": room_id, "status" : "waiting"},
        {"$push": {"members": {
            "id": user_id,
            "name": user["name"],
            "isHost": False,
            "isReady": False,
            "logs": [],
        }}},
    )

    if result.modified_count == 0:
        return error("현재 방에 참가할 수 없습니다.", 409)

    return jsonify({"status": "success", "room": get_room(room_id)})

# 8. 운동방 시작 
@app.route("/api/rooms/<room_id>/start", methods=["POST"])
@jwt_required()
def roomstart(room_id):
    register_id = get_jwt_identity()
    check_room = rooms.find_one({
        "id" : room_id,
        "members" : {
            "$elemMatch" : {
                "id" : register_id,
                "isHost" : True,
            }
        }
    })
    if check_room is None : 
            return error("유효하지 않은 방이거나, 호스트가 아닙니다.", 403)
    else : # 유효한 방 && 호스트 
        #모든 참여자의 ready 상태 확인
        all_guest_ready = True
        for member in check_room["members"] :
            if member.get("isHost", False) : continue

            if not member.get("isReady", False) : 
                all_guest_ready = False
                break
        if not all_guest_ready : 
            return error("모든 참여자가 준비하지 않았습니다", 403)

        members_id = []
        for member in check_room["members"] :
            user_id = member.get("id")
            if user_id:
                members_id.append(user_id)

        user_list = users.find(
            {"id" : {"$in": members_id}},
            {
                "_id" : 0,
                "name" : 1,
                "phone" : 1,
            }
        )

        result = rooms.update_one(
                            {
                                "id" : room_id ,
                                "status" : "waiting",
                                },
                            {"$set" : {
                                "status": "start",
                                "startedAt" : datetime.now(timezone.utc).isoformat(),
                
                                }}
                        )
        # 동시성 처리 : 
        if result.modified_count == 0 :
            return error (
                "시작 할 수 없는 방입니다", 409
            )


        for u in user_list :
            uphone = u.get("phone")
            uname = u.get("name")
            try:
                send_sms(uphone, uname)
            except Exception:
                # 문자 발송 실패가 운동 시작 자체를 막지 않도록 합니다.
                app.logger.exception("운동 시작 알림 문자 발송 실패")


        return jsonify({"status" : "success" })

# 8. 운동방 나가기 API
@app.route("/api/rooms/<room_id>/leave", methods=["POST"])
def leave_room(room_id):
    data = request.get_json() or {}
    user_id = data.get("userId", "")
    room = get_room(room_id)

    if room is None:
        return error("방을 찾을 수 없습니다.", 404)

    member = next(
        (member for member in room.get("members", []) if member["id"] == user_id),
        None,
    )

    if member is None:
        return error("방에 참가한 사용자가 아닙니다.", 404)

    if member.get("isHost"):
        return error("방장은 방 삭제하기를 이용해주세요.", 403)

    rooms.update_one(
        {"id": room_id},
        {"$pull": {"members": {"id": user_id}}},
    )

    return jsonify({"status": "success", "room": get_room(room_id)})


# 9. 운동방 삭제 API
@app.route("/api/rooms/<room_id>", methods=["DELETE"])
def delete_room(room_id):
    data = request.get_json() or {}
    user_id = data.get("userId", "")
    room = rooms.find_one({"id": room_id})

    if room is None:
        return error("방을 찾을 수 없습니다.", 404)

    is_host = room.get("hostId") == user_id or any(
        member.get("id") == user_id and member.get("isHost")
        for member in room.get("members", [])
    )

    if not is_host:
        return error("방장만 방을 삭제할 수 있습니다.", 403)

    rooms.delete_one({"id": room_id})
    return jsonify({"status": "success", "message": "방이 삭제되었습니다."})



    
            
                

# 9. 유저별 대기 상태 전환
@app.route("/api/rooms/<room_id>/ready", methods=["POST"])
@jwt_required()
def update_ready(room_id):
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    is_ready = data.get("isReady")

    if not isinstance(is_ready, bool):
        return error(
            "유효하지않은 요청입니다"
        ), 400

    result = rooms.update_one(
        {
            "id" : room_id,
            "status" : "waiting",
            "members" : {
                "$elemMatch" : {
                    "id" : user_id,
                    "isHost" : False,
                    }
                },
            },
            {
                "$set" : {"members.$.isReady" : is_ready,}
            },
    )
    return jsonify({"status" : "success"})

    
    


# 10. 개인 운동 시작, 일시정지, 종료 API
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
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # status 은 현재 운동방의 상태이므로, 별도 멤버별 자신의 운동 상태 필드가 필요함.
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


# 11. 마이페이지(히스토리)
@app.route('/api/me', methods = ["GET"])
@jwt_required()
def userme(): 
    user_id = get_jwt_identity()
    user = users.find_one({"id": user_id})
    
    return jsonify({"status" : "success", "id" : user_id, "name": user["name"]})


    
# 12. jwt 만료 콜백 함수
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    token_type = jwt_payload.get("type")

    if token_type == "access" :
        return jsonify({
            "status" : "error",
            "error_code" : "ACCESS_TOKEN_EXPIRED",
            "message" : "ACCESS TOKEN 만료됨"

                        }), 401
    return jsonify({
            "status" : "error",
            "error_code" : "REFRESH_TOKEN_EXPIRED",
            "message" : "재로그인 필요"

                        }), 401

# 12. access token 재발급 
# @app.route('/api/refresh')
# def refresh_token():
#     token_status = get
    

if __name__ == "__main__":
    app.run(debug=DEBUG, host=HOST, port=PORT)
