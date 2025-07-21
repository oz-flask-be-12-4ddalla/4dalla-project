from flask import Blueprint, request, jsonify
from app.models import Answer, User, Choice
from config import db

answers_blp = Blueprint('answers', __name__, url_prefix='/answers')

def check_duplicate(user_id, question_id):
    # 한 질문에 한 번만 답변 허용
    return Answer.query.join(Choice).filter(
        Answer.user_id == user_id,
        Choice.question_id == question_id
    ).first() is not None # True 반환 -> 중복 답변

# 설문 답변 제출 
@answers_blp.route('/', methods=['POST'])
def submit_answer():
    data = request.json
    user_id = data.get('user_id')
    choice_id = data.get('choice_id')

    user = User.query.get(user_id)
    choice = Choice.query.get(choice_id)
    if not user:
        return jsonify({'error': '유효하지 않은 유저'}), 400
    if not choice:
        return jsonify({'error': '유효하지 않은 선택지'}), 400

    question_id = choice.question_id
    if check_duplicate(user_id, question_id):
        return jsonify({'error': '이미 답변한 문항입니다.'}), 409

    answer = Answer(user_id=user_id, choice_id=choice_id)
    db.session.add(answer)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'DB 오류'}), 500

    return jsonify({'answer_id': answer.id}), 201

# 사용자별 전체 답변 조회
@answers_blp.route('/user/<int:user_id>', methods=['GET'])
def get_user_answers(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '사용자 없음'}), 404
    data = []
    for ans in Answer.query.filter_by(user_id=user_id).all():
        choice = Choice.query.get(ans.choice_id)
        data.append({
            'answer_id': ans.id,
            'choice_id': ans.choice_id,
            'question_id': choice.question_id if choice else None,
            'created_at': ans.created_at.isoformat() if ans.created_at else None
        })
    return jsonify(data)