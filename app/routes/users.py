from flask import Blueprint, request, jsonify
from ..models import User
from config import db

user_blp = Blueprint("users", __name__)

@user_blp.route("/",methods=["GET"])
def connect():
    if request.method == "GET":
        return jsonify({"message":"success Connect"})


@user_blp.route("/signup", methods=["POST"])
def signup():
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message":"이미 가입된 이메일입니다."}),400
    
    if User.query.filter_by(name=data["name"]).first():
        return jsonify({"message":"이미 가입된 이름입니다."}),400
    
    if not data.get["email"] or "@" not in data["email"]:
        return jsonify({"message":"이메일 형식이 올바르지 않습니다."}),400
    
    data = request.get_json()
    user = User(
        name =data["name"],
        email = data["email"],
        gender = data["gender"],
        age = data["age"]
    )
    db.session.add(user)
    db.session.commit()

    
    return jsonify({"message":f"{user.name}님 회원가입을 축하합니다!",
                    "user_id":user.id # 이건 왜 줘야함? 선택사항이지만 클라이언트가 새로 생성된 리소스를 식별하고 활용할 수 있도록 도와주는 좋은 API설계 습관이랍니다.
                    }),201
# 우린 초보자니까 여기서 try except문으로 리팩토링을 해보자...!