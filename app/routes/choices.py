from flask import Blueprint, request, jsonify
from models import db, Choice
from datetime import datetime

choice_blp = Blueprint('choice', __name__, url_prefix='/choices')

# 1. 선택지 전체 조회
@choice_blp.route('/', methods=['GET']) #블루프린트 생성!
def get_choices():
    choices = Choice.query.all() #모든 초이스를 디비에서 가져옴
    return jsonify([
        {
            'id': c.id,
            'question_id': c.question_id,
            'content': c.content,
            'sqe': c.sqe,
            'is_active': c.is_active
        } for c in choices
    ])

# 2. 선택지 생성
@choice_blp.route('/', methods=['POST'])
def create_choice():
    data = request.get_json()
    new_choice = Choice(
        question_id=data['question_id'],
        content=data['content'],
        sqe=data.get('sqe', 1),
        is_active=data.get('is_active', True)
    )
    db.session.add(new_choice)
    db.session.commit()
    return jsonify({'message': 'Choice created', 'id': new_choice.id}), 201

# 3. 선택지 삭제
@choice_blp.route('/<int:choice_id>', methods=['DELETE'])
def delete_choice(choice_id):
    choice = Choice.query.get_or_404(choice_id)
    db.session.delete(choice)
    db.session.commit()
    return jsonify({'message': 'Choice deleted'})
