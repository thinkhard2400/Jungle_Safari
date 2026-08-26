## 프론트엔드 라우팅용

from flask import Blueprint, render_template

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