import connection
from psycopg2 import sql

@connection.connection_handler
def get_questions(cursor):
    cursor.execute("""
                   SELECT * FROM question
                   """)
    questions = cursor.fetchall()
    return questions


#@connection.connection_handler
#def sort_questions(cursor, selection, order):
 #   cursor.execute(sql.SQL("""SELECT * FROM question ORDER BY {} {}""")
  #                 .format(sql.Identifier(selection), sql.Identifier(order)).as_string(cursor)
   # questions = cursor.fetchall()
    #return questions

@connection.connection_handler
def sort_questions(cursor, selection, order):
    cursor.execute(sql.SQL("""SELECT * FROM question ORDER BY {selection} {order} ;""")
                   .format(selection=sql.Identifier(selection), order=sql.Identifier(order)))
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
def add_new_answer(cursor, detail):
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message) 
                    VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s)
                    """,
                   detail)


@connection.connection_handler
def delete_question_and_answer(cursor, id):

    # TODO: fix bug: 'update or delete on table "question" violates foreign key constraint "question_id" on table "answer"'

    '''
    cursor.execute("""
                DELETE FROM answer
                WHERE id = %(id)s;
                """,
               {'id': id})
    '''

    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(id)s;
                    """,
                   {'id': id})

     # TODO make it work with any table



@connection.connection_handler
def edit_question(cursor, id, title, message):
    cursor.execute("""
                   UPDATE question
                   SET title = %(title)s, message = %(message)s
                   WHERE id = %(id)s;
                   """,
                   {'id': id, 'title': title, 'message': message})
