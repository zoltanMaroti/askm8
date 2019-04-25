import connection
import random
from datetime import datetime

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
    """
    Generates random and unique string. Used for id/key generation:
         - at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case character
         - it must be unique in the table (first value in every row is the id)

    Args:
        table (list): Data table to work on. First columns containing the keys.

    Returns:
        string: Random and unique string
    """

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

    # if nemtalal ide kell valami


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
