import time

from flask import Flask, render_template, redirect, request

import connection
import data_manager
import time

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def show_all_questions():
    selection = request.args.get('selection')
    # order = request.args.get('order')
    questions = data_manager.pass_questions()
    if selection is None:
        sorted_questions = connection.get_questions_file()
        return render_template('list.html', questions=sorted_questions)
    else:
        sorted_questions = sorted(questions, key=lambda item: item[selection])
        return render_template('list.html', questions=sorted_questions)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def view_question(question_id):
    selected_question = data_manager.get_question_id(connection.get_questions_file(), question_id)
    answers = connection.get_answers_file()
    if request.method == 'POST':
        new_answer = {
            'id': data_manager.generate_random(answers),
            'submission_time': int(time.time()),
            'vote_number': '1',  # TODO add vote_number counting
            'question_id': question_id,
            'message': request.form['message']
        }
        connection.write_answer_to_file(new_answer)
        return redirect(request.url)
    elif request.method == 'GET':
        return render_template('question.html', question=selected_question, title='Question', answers=answers)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html')

    if request.method == 'POST':
        questions = data_manager.pass_questions()
        new_question = {
            'id': data_manager.generate_random(questions),
            'submission_time': int(time.time()),
            'view_number': '100',  # TODO add view_number counting
            'vote_number': '1',  # TODO add vote_number counting
            'title': request.form['title'].title(),
            'message': request.form['message']
        }
        connection.write_question_to_file(new_question)
        return redirect('/')


@app.route('/question/<question_id>/edit', methods=['POST', 'GET'])
def edit_question(question_id):
    selected_question = data_manager.get_question_id(connection.get_questions_file(), question_id)
    return render_template('edit_question.html', question=selected_question)

@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    questions = connection.get_questions_file()
    updated_questions = data_manager.delete_question_by_id(question_id, questions)
    connection.delete_story_from_file(updated_questions)
    return redirect('/')

if __name__ == '__main__':
    app.run(
        debug=True
    )
