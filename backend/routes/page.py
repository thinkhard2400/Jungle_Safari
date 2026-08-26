## 프론트엔드 라우팅용

from flask import Blueprint, render_template, jsonify
import time

page_bp = Blueprint("page", __name__)

@page_bp.route("/")
def index():
    return render_template("index.html")

@page_bp.route("/login")
def login():
    return render_template("login.html")

@page_bp.route("/signup")
def signup():
    return render_template("signup.html")

@page_bp.route("/main")
def main():
    return render_template("main.html")

@page_bp.route("/room")
def room():
    return render_template("room.html")

@page_bp.route("/complete")
def complete():
    return render_template("complete.html")

@page_bp.route("/mypage")
def mypage():
    user_id = get_jwt_identity()

    me = users.find_one(
        {"id": user_id},
        {"_id": 0, "password": 0}
    )
    return render_template(
        "mypage.html",
        me=me,
    )

@page_bp.route("/sangmin/time")
def sangmin_time():
    received_at = time.time_ns()
    sent_at = time.time_ns()

    return jsonify({
        "receivedAt": received_at,
        "sentAt": sent_at,
    })

@page_bp.route("/sangmin/users/id")
def get_user_info():
    return jsonify({
        "id": "sangmin123",
        "name": "이상민",
        "roomId": "abc123"
    })

@page_bp.route("/sangmin/rooms")
def get_rooms():
    return jsonify({"rooms": []})
