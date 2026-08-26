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
    return jsonify({
        "rooms": [
            {
                "id": "abc123",
                "type": "런닝",
                "time": "08/24 23:00 ~ 23:30",
                "name": "이상민님의 방",
                "max": 4,
                "status": "start",
                "timestamp": "2026-08-24T14:00:00.000Z",
                "members": [
                    {
                        "id": "sangmin123",
                        "name": "이상민",
                        "isHost": True,
                        "isReady": True,
                        "logs": [
                            {
                                "type": "start",
                                "timestamp": "2026-08-24T14:00:00.000Z"
                            }
                        ]
                    },
                    {
                        "id": "minkyu",
                        "name": "박민규",
                        "isHost": False,
                        "isReady": True,
                        "logs": [
                            {
                                "type": "start",
                                "timestamp": "2026-08-24T14:01:10.000Z"
                            }
                        ]
                    },
                    {
                        "id": "haesun",
                        "name": "박해선",
                        "isHost": False,
                        "isReady": True,
                        "logs": [
                            {
                                "type": "start",
                                "timestamp": "2026-08-24T14:02:20.000Z"
                            },
                            {
                                "type": "pause",
                                "timestamp": "2026-08-24T14:08:40.000Z"
                            }
                        ]
                    }
                ]
            },
            {
                "id": "abc124",
                "type": "런닝",
                "time": "08/24 23:30 ~ 24:30",
                "name": "아아아악",
                "max": 4,
                "status": "wait",
                "timestamp": None,
                "members": [
                    {
                        "id": "temp1",
                        "name": "김지윤",
                        "isHost": True,
                        "isReady": True,
                        "logs": []
                    },
                    {
                        "id": "temp2",
                        "name": "최민서",
                        "isHost": False,
                        "isReady": False,
                        "logs": []
                    }
                ]
            },
            {
                "id": "abc125",
                "type": "런닝",
                "time": "08/25 20:00 ~ 21:30",
                "name": "저녁 운동",
                "max": 4,
                "status": "wait",
                "timestamp": None,
                "members": [
                    {
                        "id": "temp3",
                        "name": "이준호",
                        "isHost": True,
                        "isReady": True,
                        "logs": []
                    },
                    {
                        "id": "temp4",
                        "name": "박유진",
                        "isHost": False,
                        "isReady": True,
                        "logs": []
                    },
                    {
                        "id": "temp5",
                        "name": "한서연",
                        "isHost": False,
                        "isReady": False,
                        "logs": []
                    }
                ]
            }
        ]
    })