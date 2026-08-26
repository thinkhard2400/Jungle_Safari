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

@page_bp.route("/sangmin/time")
def sangmin_time():
    received_at = time.time_ns()
    sent_at = time.time_ns()

    return jsonify({
        "receivedAt": received_at,
        "sentAt": sent_at,
    })

@page_bp.route("/sangmin/rooms")
def sangmin_rooms():
    return jsonify({
        "rooms": [
            {
                "id": "abc123",
                "type": "런닝",
                "time": "08/24 23:00 ~ 23:30",
                "name": "이상민님의 방",
                "current": 2,
                "max": 4
            },
            {
                "id": "abc124",
                "type": "런닝",
                "time": "08/24 23:30 ~ 24:30",
                "name": "아아아악",
                "current": 1,
                "max": 4
            }
        ]
    })