from flask import Flask, render_template, redirect, request
from datetime import datetime
import connection
import data_manager
import time

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def show_all_questions():

    """
    order_selection = request.args.get('selection')
    questions = connection.get_questions_file()

    if order_selection is not None:
        questions = sorted(questions, key=lambda item: item[order_selection].lower())

    questions = data_manager.convert_numbers_to_int(questions)

    timestamps = data_manager.convert_timestamp(questions)
    return render_template('list.html', questions=questions, timestamps=timestamps)
    """

    questions = data_manager.get_questions()
    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def view_question(question_id):

    """
    selected_question = data_manager.get_question_id(connection.get_questions_file(), question_id)
    answers = connection.get_answers_from_file()

    if request.method == 'POST':
        new_answer = {
            'id': data_manager.generate_random(answers),
            'submission_time': int(time.time()),
            'vote_number': '1',  # TODO add vote_number counting
            'question_id': question_id,
            'message': request.form['message'],
            'vote': 0
        }
        connection.write_answer_to_file(new_answer)
        return redirect(request.url)

    elif request.method == 'GET':
        return render_template('question.html', question=selected_question, title='Question', answers=answers, question_id=question_id)
    """

    if request.method == 'GET':
        selected_question = data_manager.get_selected_question(question_id)
        answers = data_manager.get_answers()
        return render_template('question.html', question=selected_question, answers=answers)

    elif request.method == 'POST':
        new_answer = {
            'submission_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'vote_number': 0,
            'question_id': question_id,
            'message': request.form['message'],
        }
        data_manager.add_new_answer(new_answer)
        return redirect(request.url)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html', title='Ask Something')

    if request.method == 'POST':
        new_question = {
            'submission_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'view_number': 100,  # TODO add view_number counting
            'vote_number': 1,  # TODO add vote_number counting
            'title': request.form['title'],
            'message': request.form['message']
        }
        data_manager.add_new_question(new_question)
        return redirect('/')


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect('/')




"""
@app.route('/question/<question_id>/edit', methods=['POST', 'GET'])
def edit_question(question_id):
    selected_question = data_manager.get_question_id(connection.get_questions_file(), question_id)
    return render_template('edit-question.html', question=selected_question, title='Edit')


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    questions = connection.get_questions_file()
    updated_questions = data_manager.delete_question_by_id(question_id, questions)
    connection.delete_story_from_file(updated_questions)
    return redirect('/')


@app.route('/question/<question_id>/<answer_id>/vote')
def vote_answer(question_id,answer_id):
    answers = connection.get_answers_file()
    for answer in answers:
        if answer['id'] == answer_id:
            answer['vote'] = str(int(answer['vote']) + 1)
    return redirect('/question/<question_id>')
"""

if __name__ == '__main__':
    app.run(
        debug=True
    )
