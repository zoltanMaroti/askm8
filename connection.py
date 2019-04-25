import csv

QUESTION_FIELD_NAMES = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_FIELD_NAMES = ['id', 'submission_time', 'vote_number', 'question_id', 'message','image']


def get_questions_file():
    with open('static/question.csv') as file:
        csv_reader = csv.DictReader(file)
        return list(csv_reader)


def get_answers_file():
    with open('static/answer.csv') as file:
        csv_reader = csv.DictReader(file)
        return list(csv_reader)


def write_question_to_file(question):
    with open('static/question.csv', "a") as file:
        csv_writer = csv.DictWriter(file, fieldnames=QUESTION_FIELD_NAMES)
        csv_writer.writerow(question)


def write_answer_to_file(answer):
    with open('static/answer.csv', "a") as file:
        csv_writer = csv.DictWriter(file, fieldnames=ANSWER_FIELD_NAMES)
        csv_writer.writerow(answer)


def delete_story_from_file(question):
    with open('static/question.csv', "w") as file:
        csv_writer = csv.DictWriter(file, fieldnames=QUESTION_FIELD_NAMES)
        csv_writer.writeheader()
        csv_writer.writerows(question)