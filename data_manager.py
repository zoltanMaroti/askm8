import connection
from psycopg2 import sql


@connection.connection_handler
def get_questions(cursor):
    cursor.execute("""
                   SELECT * FROM question
                   ORDER BY submission_time DESC;
                   """)
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def sort_questions(cursor, selection, order):
    cursor.execute(sql.SQL("""SELECT * FROM question 
                              ORDER BY {selection} {order};""").format(selection=sql.SQL(selection), order=sql.SQL(order)))
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_answers(cursor):
    cursor.execute("""
                   SELECT * FROM answer
                   ORDER BY submission_time ASC;
                   """)
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def get_comments(cursor):
    cursor.execute("""
                    SELECT * FROM comment
                    ORDER BY submission_time ASC;
                    """)
    comments = cursor.fetchall()
    return comments


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
def last_questions(cursor, amount):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY submission_time DESC
                    LIMIT %(amount)s;
                    """,
                   {'amount': amount})
    last_question = cursor.fetchall()
    return last_question


@connection.connection_handler
def get_selected_answer(cursor, id):
    cursor.execute('''
                    SELECT * FROM answer
                    WHERE id = %(id)s;
                    ''',
                   {'id': id})
    selected_answer = cursor.fetchone()
    return selected_answer


@connection.connection_handler
def add_new_question(cursor, detail):
    cursor.execute("""
                   INSERT INTO question (submission_time, view_number, vote_number, title, message)
                   VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s)
                   """,
                   detail)


@connection.connection_handler
def add_new_answer(cursor, detail):
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message) 
                    VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s)
                    """,
                   detail)


@connection.connection_handler
def add_new_comment(cursor, detail):
    cursor.execute("""
                    INSERT INTO comment (question_id, message, submission_time, edited_number)
                    VALUES (%(question_id)s, %(message)s, %(submission_time)s, %(edited_number)s);
                    """, detail)


@connection.connection_handler
def edit_answer(cursor, id, message):
    cursor.execute("""
                    UPDATE answer
                    SET message = %(message)s
                    WHERE id = %(id)s;""",
                   {'id': id, 'message': message})


@connection.connection_handler
def delete_question_and_answer(cursor, id):
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(id)s;
                    """,
                   {'id': id})


@connection.connection_handler
def edit_question(cursor, id, title, message):
    cursor.execute("""
                   UPDATE question
                   SET title = %(title)s, message = %(message)s
                   WHERE id = %(id)s;
                   """,
                   {'id': id, 'title': title, 'message': message})


@connection.connection_handler
def get_result(cursor, search):
    search = '%' + search + '%'
    cursor.execute("""SELECT * FROM question 
                              WHERE title LIKE %(search)s ;""", {"search": search})
    search_result = cursor.fetchall()
    return search_result


'''
@connection.connection_handler
def get_result(cursor, question):
    question = '%' + question + '%'
    cursor.execute("""SELECT q.title, q.message, a.message FROM
                    (SELECT title, message FROM question
                    WHERE title LIKE %(question)s) AS q,
                    (SELECT message FROM answer
                    WHERE message LIKE %(question)s) AS a
                    ;""", {"question": question})
    questions = cursor.fetchall()
    return questions
'''


@connection.connection_handler
def upvote_question(cursor, id, vote_number):
    cursor.execute("""
                       UPDATE question
                       SET vote_number = %(vote_number)s
                       WHERE id = %(id)s;
                       """,
                   {'id': id, 'vote_number': vote_number})


@connection.connection_handler
def upvote_answer(cursor, id, vote_number):
    cursor.execute("""
                       UPDATE answer
                       SET vote_number = %(vote_number)s
                       WHERE id = %(id)s;
                       """,
                   {'id': id, 'vote_number': vote_number})


@connection.connection_handler
def view_counter(cursor, id):
    cursor.execute("""
                   UPDATE question
                   SET view_number = view_number + 1
                   WHERE id = %(id)s;
                   """, {'id': id})


@connection.connection_handler
def save_user_data(cursor, username, hashed_pass, email):
    cursor.execute("""
                    INSERT INTO users (username, password, email)
                    VALUES (%(username)s, %(password)s, %(email)s)
                    """, {'username': username, 'password': hashed_pass, 'email': email})


@connection.connection_handler
def get_hash(cursor, username):
    cursor.execute("""
                    SELECT password FROM users
                    WHERE username = %(username)s
                    """, {'username': username})
    hash = cursor.fetchone()
    return hash

