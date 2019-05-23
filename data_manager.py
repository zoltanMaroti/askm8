from psycopg2 import sql

import connection
import util


@connection.connection_handler
def get_ordered_data(cursor, table, order_by, direction):
    cursor.execute(sql.SQL("""SELECT * FROM {table} 
                                  ORDER BY {order_by} {direction};
                                  """).format(table=sql.SQL(table), order_by=sql.SQL(order_by),
                                              direction=sql.SQL(direction)))
    data = cursor.fetchall()
    return data


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
def get_selected_answer(cursor, id):
    cursor.execute('''
                    SELECT * FROM answer
                    WHERE id = %(id)s;
                    ''',
                   {'id': id})
    selected_answer = cursor.fetchone()
    return selected_answer


@connection.connection_handler
def get_selected_comment(cursor, id):
    cursor.execute('''
                    SELECT * FROM comment
                    WHERE id = %(id)s;
                    ''',
                   {'id': id})
    selected_answer = cursor.fetchone()
    return selected_answer


@connection.connection_handler
def get_selected_row(cursor, id, table):
    cursor.execute(sql.SQL('''
                    SELECT * FROM {table}
                    WHERE id = {id};
                    ''').format(id=sql.SQL(id), table=sql.SQL(table)))
    selected_row = cursor.fetchall()
    return selected_row


@connection.connection_handler
def get_result(cursor, search):
    search = '%' + search + '%'
    cursor.execute("""SELECT DISTINCT (q.title) AS q_title, q.id AS q_id
                        FROM question q JOIN answer a on q.id = a.question_id
                              WHERE q.title LIKE %(search)s OR q.message LIKE %(search)s 
                              OR a.message LIKE %(search)s ;""", {"search": search})
    search_result = cursor.fetchall()
    return search_result


@connection.connection_handler
def sort_questions(cursor, selection, order):
    cursor.execute(sql.SQL("""SELECT * FROM question 
                              ORDER BY {selection} {order};""").format(selection=sql.SQL(selection),
                                                                       order=sql.SQL(order)))
    questions = cursor.fetchall()
    return questions


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
def add_new_question(cursor, detail):
    cursor.execute("""
                   INSERT INTO question (submission_time, view_number, vote_number, title, message, user_id)
                   VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(user_id)s)
                   """,
                   detail)


@connection.connection_handler
def add_new_answer(cursor, detail):
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message, user_id) 
                    VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(user_id)s)
                    """,
                   detail)


@connection.connection_handler
def add_new_comment(cursor, detail):
    cursor.execute("""
                    INSERT INTO comment (question_id, message, submission_time, edited_number, user_id)
                    VALUES (%(question_id)s, %(message)s, %(submission_time)s, %(edited_number)s, %(user_id)s);
                    """, detail)



@connection.connection_handler
def insert_data(cursor, table, data):
    values = util.make_string(data)
    cursor.execute(sql.SQL(("""
                       INSERT INTO {table}
                       VALUES (%(values)s);
                       """).format(table=sql.SQL(table), values=sql.SQL(values))))


@connection.connection_handler
def edit_answer(cursor, id, message):
    cursor.execute("""
                    UPDATE answer
                    SET message = %(message)s
                    WHERE id = %(id)s;""",
                   {'id': id, 'message': message})


@connection.connection_handler
def edit_question(cursor, id, title, message):
    cursor.execute("""
                   UPDATE question
                   SET title = %(title)s, message = %(message)s
                   WHERE id = %(id)s;
                   """,
                   {'id': id, 'title': title, 'message': message})


@connection.connection_handler
def edit_comment(cursor, id, message):
    cursor.execute("""
                    UPDATE comment
                    SET message = %(message)s
                    WHERE id = %(message)s;
                    """,
                   {'id': id, 'message': message})


@connection.connection_handler
def delete_question_and_answer(cursor, id):
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(id)s;
                    """,
                   {'id': id})


@connection.connection_handler
def delete_row(cursor, id, table):
    cursor.execute(sql.SQL("""
                    DELETE FROM {table}
                    WHERE id = {id}
                    """).format(id=sql.SQL(id), table=sql.SQL(table)))


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


@connection.connection_handler
def get_users(cursor):
    cursor.execute("""
                    SELECT username from users;
                    """)
    usernames = cursor.fetchall()
    return usernames


@connection.connection_handler
def get_emails(cursor):
    cursor.execute("""
                    SELECT email from users;
                    """)
    emails = cursor.fetchall()
    return emails


@connection.connection_handler
def get_user_id(cursor, username):
    cursor.execute("""
                    SELECT id FROM users
                    WHERE username = %(username)s;
                    """, {'username': username})
    user_id = cursor.fetchone()
    return user_id

@connection.connection_handler
def get_username(cursor, id):
    cursor.execute("""
                    SELECT username FROM users
                    WHERE id = %(id)s;
                    """, {'id': id})
    username = cursor.fetchone()
    return username