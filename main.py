from os import listdir

from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user
from flask_wtf import FlaskForm

from wtforms import PasswordField, StringField, IntegerField, EmailField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired

from data import db_session
from data.jobs import Job
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# session.permanent = True
login_manager = LoginManager()
login_manager.init_app(app)

LIST_OF_TEMPLATES = list(map(lambda x: x.split('.')[0], listdir('templates')))


def return_links():
    return LIST_OF_TEMPLATES


def main():
    db_session.global_init("./db/mars_explorer.sqlite")
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/base')
@app.route('/index')
def index():
    db_session.global_init("db/mars_explorer.sqlite")
    db_sess = db_session.create_session()
    params = {
        'title': 'Начальная страница',
        'navbar_title': 'Миссия Колонизация Марса',
        'data': None,
        'hrefs': return_links(),
        'jobs': [job for job in db_sess.query(Job)],
        'users': [user for user in db_sess.query(User)]
    }
    return render_template('index.html', **params)


class RegisterForm(FlaskForm):
    email_login = EmailField('Email/Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Регистрация')


@app.route('/register', methods=['GET', 'POST'])
def register():
    db_session.global_init("db/mars_explorer.sqlite")
    form = RegisterForm()
    params = {
        'title': 'Регистрация',
        'navbar_title': 'Миссия Колонизация Марса',
        'form': form,
        'hrefs': return_links()
    }
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('register.html', **params,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email_login.data).first():
            return render_template('register.html', **params,
                                   message="Такой пользователь уже существует")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email_login.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return 'Registration complete!!!!!!!!!!!!!!!!'
    return render_template('register.html', **params)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@app.route('/login', methods=['GET', 'POST'])
def login():
    db_session.global_init("db/mars_explorer.sqlite")
    form = LoginForm()
    params = {
        'title': 'Авторизация',
        'navbar_title': 'Миссия Колонизация Марса',
        'form': form,
        'hrefs': return_links()
    }
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               **params)
    return render_template('login.html', **params)


class JobForm(FlaskForm):
    job = StringField('Работа', validators=[DataRequired()])
    leader_id = StringField('Индетификатор лидера', validators=[DataRequired()])
    work_size = IntegerField('Размер работы (в часах)', validators=[DataRequired()])
    collaborators = StringField('Участники', validators=[DataRequired()])
    start_date = DateField('Дата начала')
    end_date = DateField('Дата конца', validators=[DataRequired()])
    is_finished = BooleanField('Закончена ли работа?')
    submit = SubmitField('Создать')
    


@app.route('/create_job', methods=["GET", "POST"])
def create_job():
    db_session.global_init("db/mars_explorer.sqlite")
    form = JobForm()
    params = {
        'title': 'Создание записи о работе',
        'navbar_title': 'Миссия Колонизация Марса',
        'form': form,
        'hrefs': return_links()
    }
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        leader = db_sess.query(User).filter(User.id == form.leader_id.data).first()
        if leader is None:
            return render_template('create_job.html', **params, message="Лидер не найден!")
        job = Job(
            leader = leader,
            job = form.job.data,
            work_size = form.work_size.data,
            collaborators = form.collaborators.data,
            start_date = form.start_date.data,
            end_date = form.end_date.data,
            is_finished = form.is_finished.data,
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('create_job.html', **params)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')


if __name__ == '__main__':
    main()
