from flask import Blueprint, request, jsonify
from config import db
from models import Choice
from datetime import datetime

choices_blp = Blueprint('choice', __name__)

# 질문 생성

@choices_blp.route('/choice', methods=['POST']) #method는 복수형으로!
def create_choice():
    data = request.get_json()
    new_choice = Choice(
        question_id = data['question_id'],
        content = data['content'],
        sqe = data.get('sqe', 1),
        is_active = data.get('is_active', True)
    )
    db.session.add(new_choice)
    db.session.commit()

    return jsonify({
        "message": "Content: 새로운 선택지 choice Success Create"
    })
