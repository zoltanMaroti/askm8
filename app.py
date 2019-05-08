from flask import Flask, render_template, redirect, request
from datetime import datetime
import data_manager

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['GET', 'POST'])
def show_all_questions():
    if request.method == 'GET':
        questions = data_manager.sort_questions('submission_time', 'DESC', limit='limited')
        return render_template('list.html', questions=questions, selection='submission_time', order='DESC')
    elif request.method == 'POST':
        questions = data_manager.sort_questions(request.form['selection'], request.form['order'], limit='limited')
        return render_template('list.html', questions=questions, selection=request.form['selection'], order=request.form['order'])


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def view_question(question_id):

    if request.method == 'GET':
        selected_question = data_manager.get_selected_question(question_id)
        answers = data_manager.sort_answers('submission_time', 'ASC')
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


@app.route('/question/<question_id>/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(question_id, answer_id):
    selected_question = data_manager.get_selected_question(question_id)
    selected_answer = data_manager.get_selected_answer(answer_id)
    if request.method == 'POST':
        data_manager.edit_answer(answer_id, request.form['message'])
        return redirect('/question/' + question_id)
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
        result = data_manager.get_result(request.form['search'])
        return render_template("result.html", results=result)


@app.route('/question/<question_id>/new-comment')
def add_comment(question_id):
    selected_question = data_manager.get_selected_question(question_id)
    if request.method == 'POST':
        return 'get rekt'
    return render_template("add-comment.html", question=selected_question)


@app.route('/question/<question_id>/<vote_number>')
def upvote_question(question_id, vote_number):
    upvoted = int(vote_number) + 1
    data_manager.upvote_question(question_id, vote_number=upvoted)
    return redirect(request.referrer)


@app.route('/question/<question_id>/<answer_id>/<vote_number>')
def upvote_answer(question_id, answer_id, vote_number):
    upvoted = int(vote_number) + 1
    data_manager.upvote_answer(answer_id, vote_number=upvoted)
    return redirect(request.referrer)


@app.route('/list/unlimit/<selection>/<order>')
def unlimited(selection, order):
    if request.method == 'GET':
        questions = data_manager.sort_questions('submission_time', 'DESC', limit='unlimited')
        return render_template('list.html', questions=questions, selection='submission_time', order='DESC')
    elif request.method == 'POST':
        questions = data_manager.sort_questions(request.form['selection'], request.form['order'], limit='unlimited')
        return render_template('list.html', questions=questions, selection=selection, order=order)



if __name__ == '__main__':
    app.run(
        debug=True
    )
