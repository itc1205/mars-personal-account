from os import listdir

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, IntegerField, EmailField, SubmitField
from wtforms.validators import DataRequired

from data import db_session
from data.jobs import Jobs
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

STATIC_PATH = 'static'
TEMPLATE_PATH = 'templates'
LIST_OF_TEMPLATES = list(map(lambda x: x.split('.')[0], listdir('templates')))
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def return_links():
    return LIST_OF_TEMPLATES


def main():
    db_session.global_init("db/mars_explorer.sqlite")
    app.run()


@app.route('/base')
def base():
    return render_template('base.html')


@app.route('/')
@app.route('/base')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    params = {
        'title': 'Лист с профессиями',
        'navbar_title': 'Миссия Колонизация Марса',
        'data': None,
        'hrefs': return_links(),
        'jobs': [job for job in db_sess.query(Jobs)],
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
    form = RegisterForm()
    params = {
        'title': 'Лист с профессиями',
        'navbar_title': 'Миссия Колонизация Марса',
        'form': form
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


if __name__ == '__main__':
    main()
