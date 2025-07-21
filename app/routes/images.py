from flask import Blueprint, jsonify, request
from config import db
from app.models import Image

images_blp = Blueprint("images",__name__)

@images_blp.route("/image", methods=["POST"])
def create_image():
    data = request.get_json()

    # 유효성 검사
    if not data.get("url") or not data.get("type"):
        return jsonify({"message": "url 또는 type이 누락되었습니다."}), 400

    # 이미지 객체 생성
    image = Image(
        url=data["url"],
        type=data["type"]
    )

    # DB에 저장
    try:
        db.session.add(image)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "DB 저장 중 오류가 발생했습니다.", "error": str(e)}), 500

    return jsonify({"message" :f"ID: {image.id} Image Success Create" }), 201


@images_blp.route("/image/main", methods=["GET"])
def get_main_image():
    image = Image.query.filter_by(type="main").first()

    if not image : 
        return jsonify({"message" : "메인 이미지가 없습니다."}), 404
    return jsonify({"image":image.url})