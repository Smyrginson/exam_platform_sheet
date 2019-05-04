from flask import render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField
from functools import wraps

from models.exam import ExamModel, QuestionModel
from models.user import UserModel
from models.answer import AnswerModel

from resources.user import UserRegister, UserLogin

from app import app


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')


class CreateUser(Form):
    username = StringField('username')
    password = PasswordField('password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = CreateUser(request.form)
    if request.method == 'POST':
        user = UserRegister.register(username=form.username.data, password=form.password.data)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = UserLogin.login(request.form['username'], request.form['password'])
        if user:
            session['login'] = True
            session['username'] = user.username
            app.logger.info(f'zalogowalews sie jako {session["username"]}')
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_sheet():
    exam = ExamModel()
    exam.owner = UserModel.find_by_name(session['username'])
    exam.save_to_db()
    return redirect(f'/edit/{exam.id}')


@app.route('/manage')
@login_required
def manage():
    if request.method == 'POST':
        pass
    user = UserModel.find_by_name(session['username'])
    return render_template('manage.html', exams=user.get_exams())


@app.route('/edit/<int:_id>', methods=['GET', 'POST'])
@login_required
def edit_sheet(_id):
    exam = ExamModel.find_by_id(_id)
    if request.method == 'POST':
        exam.exam_name = request.form['title']
        for question in exam.get_questions():
            question.question = request.form[f'question{question.id}']
            question.answer1 = request.form[f'answer1{question.id}']
            question.answer2 = request.form[f'answer2{question.id}']
            question.answer3 = request.form[f'answer3{question.id}']
            question.answer4 = request.form[f'answer4{question.id}']
            question.correct_answer = request.form[f'correct{question.id}']
            question.save_to_db()

        if request.form['action'] == '+add question':
            question = QuestionModel()
            question.exam = exam
            question.save_to_db()

        user = UserModel.find_by_name(session['username'])
        exam.owner = user
        user.save_to_db()
        exam.save_to_db()
    return render_template('create.html', exam=exam, questions=exam.get_questions())


@app.route('/delete/<int:_id>', methods=['GET', 'POST'])
@login_required
def delete_sheet(_id):
    exam = ExamModel.find_by_id(_id)
    exam.delete_from_db()
    return redirect(url_for('manage'))


@app.route('/add_question/<int:_id>')
@login_required
def add_question(_id):
    exam = ExamModel.find_by_id(_id)
    question = QuestionModel()
    question.exam = exam
    exam.save_to_db()
    question.save_to_db()
    return redirect(f'/edit/{exam.id}')


@app.route('/remove_question/<int:question_id>')
@login_required
def remove_question(question_id):
    exam = ExamModel.remove_question(question_id)
    return redirect(f'/edit/{exam.id}')


@app.route('/examboard')
@login_required
def examboard():
    user = UserModel.find_by_name(session['username'])
    exams = ExamModel.find_others_courses(user)
    return render_template('examboard.html', exams=exams, user=user)


@app.route('/examsheet/<int:sheet>', methods=['GET', 'POST'])
@login_required
def examsheet(sheet):
    exam = ExamModel.find_by_id(sheet)
    user = UserModel.find_by_name(session['username'])
    questions = exam.get_questions()
    if request.method == 'POST':
        for question in questions:
            answer = AnswerModel.find_answer(user=user, exam=exam, question=question)
            if not answer:
                answer = AnswerModel()

            answer.user = user
            answer.exam = exam
            answer.question = question
            try:
                answer.answer = int(request.form[f'answer{question.id}'])
                if question.correct_answer == answer.answer:
                    if not answer.is_correct:
                        user.points = user.points + 1
                    answer.is_correct = True
                answer.save_to_db()
            except ValueError as err:
                print(f'Question {question.id} don`t have answer')

    return render_template('examsheet.html', exam=exam, questions=questions)


@app.route('/scores')
def scores():
    scores_list = UserModel.take_score()
    return render_template('scores.html', scores=scores_list)

