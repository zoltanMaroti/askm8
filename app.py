from flask import Flask, render_template, redirect, request, url_for
import connection
import data_manager
import time

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def show_all_questions():
    selection = request.args.get('selection')
    # order = request.args.get('order')
    questions = connection.get_questions_file()
    if selection is None:
        sorted_questions = connection.get_questions_file()
        return render_template('list.html', questions=sorted_questions)
    else:
        sorted_questions = sorted(questions, key=lambda item: item[selection].lower())
        return render_template('list.html', questions=sorted_questions)




@app.route('/question/<question_id>')
def view_question(question_id):
    selected_question = data_manager.get_question_id(connection.get_questions_file(), question_id)
    return render_template('question.html', question=selected_question, title='Question')


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html')

    if request.method == 'POST':
        new_question = {
                        'id': len(connection.get_questions_file()),
                        'submission_time': int(time.time()),
                        'view_number': '100',  # TODO add view_number counting
                        'vote_number': '1',  # TODO add vote_number counting
                        'title': request.form['title'].lower(),
                        'message': request.form['message']
                       }
        connection.write_question_to_file(new_question)
        return redirect('/')


@app.route('/question/<question_id>/new-answer')
def answer_question(question_id):  # TODO finish answer posting
    return render_template('answer.html')


@app.route('/list')
def order():
    # selection = request.args('selection')
    # order = request.args.get('order')
    # questions = connection.get_questions_file()
    pass




if __name__ == '__main__':
    app.run(
        debug=True
    )
