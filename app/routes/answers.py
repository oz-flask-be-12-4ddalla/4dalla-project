from flask import Blueprint, request, jsonify
from app.models import Answer
from config import db

answers_blp = Blueprint('answers', __name__, url_prefix='/submit')

# def check_duplicate(user_id, question_id):
#     # 한 질문에 한 번만 답변 허용
#     return Answer.query.join(Choice).filter(
#         Answer.user_id == user_id,
#         Choice.question_id == question_id
#     ).first() is not None # True 반환 -> 중복 답변

# 설문 답변 제출 
@answers_blp.route('/', methods=['POST'])
def submit_answers():
    data_list = request.get_json()

    if not isinstance(data_list, list):
        return jsonify({"message": "Request body must be a list of answers"}), 400

    try:
        created_user_id = None

        for data in data_list:
            user_id = data.get("user_id")
            choice_id = data.get("choice_id")

            if user_id is None or choice_id is None:
                return jsonify({"message": "Missing user_id or choice_id"}), 400

            answer = Answer(user_id=user_id, choice_id=choice_id)
            db.session.add(answer)

            # 첫 번째 user_id만 메시지에 활용 (모든 answer가 같은 user_id라면)
            if created_user_id is None:
                created_user_id = user_id

        db.session.commit()

        return jsonify({"message": f"User:{created_user_id}'s answers Success Create"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error occurred: {str(e)}"}), 500
    
    
    # 중복 방지
    # question_id = choice.question_id
    # if check_duplicate(user_id, question_id):
    #     return jsonify({'error': '이미 답변한 문항입니다.'}), 409



    # try:
    #     db.session.commit()
    # except Exception:
    #     db.session.rollback()
    #     return jsonify({'error': "DB 저장 중 오류가 발생했습니다.", "error": str(e)}), 500



# # 사용자별 전체 답변 조회
# @answers_blp.route('/user/<int:user_id>', methods=['GET'])
# def get_user_answers(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({'error': '사용자 없음'}), 404
#     data = []
#     for ans in Answer.query.filter_by(user_id=user_id).all():
#         choice = Choice.query.get(ans.choice_id)
#         data.append({
#             'answer_id': ans.id,
#             'choice_id': ans.choice_id,
#             'question_id': choice.question_id if choice else None,
#             'created_at': ans.created_at.isoformat() if ans.created_at else None
#         })
#     return jsonify(data)