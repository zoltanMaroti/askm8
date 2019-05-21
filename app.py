from flask import Flask, render_template, redirect, request, url_for, escape
import data_manager
import util
import error_handle

app = Flask(__name__)


@app.route('/list', methods=['GET', 'POST'])
def show_all_questions():
    order_column = request.args.get('selection', 'submission_time')
    order_direction = request.args.get('order', 'DESC')

    questions = data_manager.sort_questions(order_column, order_direction)
    return render_template('list.html', questions=questions, selection=order_column, order=order_direction)


@app.route('/')
def show_limited_question():
    questions = data_manager.last_questions(5)
    return render_template('list.html', questions=questions, limit='limited')


@app.route('/question/<question_id>')
def view_question(question_id):
    data_manager.view_counter(question_id)
    selected_question = data_manager.get_selected_question(question_id)
    answers = data_manager.get_answers()
    comments = data_manager.get_comments()
    return render_template('question.html', question=selected_question, answers=answers, comments=comments, title='Question')


@app.route('/question/<question_id>', methods=['POST'])
def view_question_post(question_id):
    new_answer = {
        'submission_time': util.get_current_datetime(),
        'vote_number': 0,
        'question_id': question_id,
        'message': escape(request.form['message']),
    }
    data_manager.add_new_answer(new_answer)
    return redirect(request.url)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html', title='Ask Something')

    if request.method == 'POST':
        new_question = {
            'submission_time': util.get_current_datetime(),
            'view_number': 0,
            'vote_number': 0,
            'title': escape(request.form['title']),
            'message': escape(request.form['message'])
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
    return render_template('edit-answer.html', question=selected_question, answer=selected_answer, title='Edit Answer')


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
    return render_template('edit-question.html', question=selected_question, title='Edit Question')


@app.route('/result', methods=['GET', 'POST'])
def show_result():
    if request.method == 'POST':
        questions = data_manager.get_questions()
        result = data_manager.get_result(escape(request.form['search']))
        return render_template("result.html", results=result, title='Results', questions=questions)


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment(question_id):
    selected_question = data_manager.get_selected_question(question_id)
    if request.method == 'POST':
        new_comment = {
            'question_id': question_id,
            'message': escape(request.form['message']),
            'submission_time': util.get_current_datetime(),
            'edited_number': 0
        }
        data_manager.add_new_comment(new_comment)
        return redirect('/question/' + question_id)
    return render_template("add-comment.html", question=selected_question, title='Add Comment')


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


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        errors = error_handle.check_error(username=username, password=password, confirm_password=confirm_password, email=email)
        if len(errors) > 0:
            return render_template('register.html', error=errors)
        hashed_pass = util.hash_pass(password)
        data_manager.save_user_data(username=username, hashed_pass=hashed_pass, email=email)
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration')


if __name__ == '__main__':
    app.run(
        debug=True
    )
