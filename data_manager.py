import connection

'''
def pass_questions():
    ord_dict = connection.get_questions_file()
    for question in ord_dict:
        question['vote_number'] = int(question['vote_number'])
        question['view_number'] = int(question['view_number'])
        question['submission_time'] = int(question['submission_time'])
    return ord_dict


def get_question_id(questions, question_id):
    for question in questions:
        if question_id == question['id']:
            return question


def get_ids(odered_dic):
    ids = []
    for item in odered_dic:
        ids.append(item['id'])
    return ids


def generate_random(table):

    SPECIALCHARS = "!@#$%^&*()[]:,.<>?"
    NUMBERS = '0123456789'
    LETTERS = 'abcdefghijklmnopqrtuvwxyz'

    generated = ''

    ids = get_ids(table)

    reference = ids[0]
    unique = False

    while not unique:
        generated = ''
        for character in reference:
            if character in LETTERS:
                generated += random.choice(LETTERS)
            elif character in LETTERS.upper():
                generated += random.choice(LETTERS.upper())
            elif character in NUMBERS:
                generated += str(random.randint(0, 9))
            elif character in SPECIALCHARS:
                generated += random.choice(SPECIALCHARS)
            elif character == '-':
                generated += '-'
        if generated not in ids:
            unique = True

    return generated


def delete_question_by_id(question_id, questions):
    updated_questions = []
    for question in questions:
        if question['id'] != question_id:
            updated_questions.append(question)
    return updated_questions


def convert_timestamp(questions):
    timestamps = []
    for question in questions:
        timestamps.append(datetime.fromtimestamp(question['submission_time']).strftime('%Y-%m-%d %H:%M:%S'))
    return timestamps


def convert_numbers_to_int(questions):
    for question in questions:
        question['vote_number'] = int(question['vote_number'])
        question['view_number'] = int(question['view_number'])
        question['submission_time'] = int(question['submission_time'])
    return questions
'''


@connection.connection_handler
def get_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question;
                   """)
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_answers(cursor):
    cursor.execute("""
                   SELECT * FROM answer;
                   """)
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def get_selected_question(cursor, id):
    cursor.execute("""
                   SELECT * FROM question
                   WHERE id = %(id)s;
                   """,
                   {'id': id})
    selected_question = cursor.fetchone()
    return selected_question


@connection.connection_handler
def add_new_question(cursor, detail):
    cursor.execute("""
                   INSERT INTO question (submission_time, view_number, vote_number, title, message)
                   VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s)
                   """,
                   detail)

@connection.connection_handler
def delete_question(cursor, id):
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(id)s;
                    """,
                   {'id': id})

