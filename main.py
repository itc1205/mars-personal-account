from flask import Flask, render_template
from os import listdir

from data import db_session
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

STATIC_PATH = 'static'
TEMPLATE_PATH = 'templates'
LIST_OF_TEMPLATES = list(map(lambda x: x.split('.')[0], listdir('templates')))
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

def return_links():
    return LIST_OF_TEMPLATES

def return_all_users(db_name='db/mars_explorer.sqlite'):
    db_session.global_init(db_name)
    db_sess = db_session.create_session()
    users = []
    for user in db_sess.query(User).all():
        users.append(user)
    return users



def main():
    db_session.global_init("db/mars_explorer.sqlite")
    app.run()

@app.route('/base')
def base():
    return render_template('base.html')


@app.route('/')
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
    print(params['jobs'])
    return render_template('index.html', **params)


if __name__ == '__main__':
    main()
