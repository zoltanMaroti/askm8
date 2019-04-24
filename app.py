from flask import Flask, render_template, redirect, request, url_for
import connection
import data_manager
import time

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def show_all_questions():
    questions = connection.get_questions_file()
    return render_template('list.html', questions=questions)


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
        questions = connection.get_questions_file()
        new_question = {
            'id': data_manager.generate_random(questions),
            'submission_time': int(time.time()),
            'view_number': '100',  # TODO add view_number counting
            'vote_number': '1',  # TODO add vote_number counting
            'title': request.form['title'],
            'message': request.form['message']
        }
        connection.write_question_to_file(new_question)
        return redirect('/')


if __name__ == '__main__':
    app.run(
        debug=True
    )
