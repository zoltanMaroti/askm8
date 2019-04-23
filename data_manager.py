import connection


def get_question_id(questions, question_id):
    for question in questions:
        if question_id == question['id']:
            return question

    # if nemtalal ide kell valami
