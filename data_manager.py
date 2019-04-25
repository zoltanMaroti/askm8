import connection
import random

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