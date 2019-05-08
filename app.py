from flask import Flask, render_template, redirect, request
from datetime import datetime
import data_manager

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['GET', 'POST'])
def show_all_questions():
    if request.method == 'GET':
        questions = data_manager.get_questions()
        return render_template('list.html', questions=questions)

    elif request.method == 'POST':
        questions = data_manager.sort_questions(request.form['selection'], request.form['order'])
        return render_template('list.html', questions=questions)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def view_question(question_id):

    if request.method == 'GET':
        data_manager.view_counter(question_id)
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
            'view_number': 0,
            'vote_number': 1,  # TODO add vote_number counting
            'title': request.form['title'],
            'message': request.form['message']
        }
        data_manager.add_new_question(new_question)
        return redirect('/')


@app.route('/question/<question_id>/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(question_id, answer_id):
    selected_question = data_manager.get_selected_question(question_id)
    selected_answer = data_manager.get_selected_answer(answer_id)
    if request.method == 'POST':
        data_manager.edit_answer(answer_id, request.form['message'])
        return redirect('/question/'+ question_id)
    return render_template('edit-answer.html', question=selected_question, answer=selected_answer)


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_question_and_answer(question_id)
    return redirect('/')


@app.route('/question/<question_id>/edit', methods=['POST', 'GET'])
def edit_question(question_id):
    selected_question = data_manager.get_selected_question(question_id)
    if request.method == 'POST':
        data_manager.edit_question(question_id, request.form['title'], request.form['message'])
        return redirect('/list')
    return render_template('edit-question.html', question=selected_question)


@app.route('/result', methods=['GET', 'POST'])
def show_result():
    if request.method == 'POST':
        questions = data_manager.get_questions()
        result = data_manager.get_result(request.form['search'])
        return render_template("result.html", results=result, questions=questions)


if __name__ == '__main__':
    app.run(
        debug=True
    )
