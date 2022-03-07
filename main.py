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

def print_all_users(db_name='db/mars_explorer.sqlite'):
    db_session.global_init(db_name)
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        print(user)


def main():
    db_session.global_init("db/mars_explorer.sqlite")
    # app.run()
    db_sess = db_session.create_session()
    ###################################
    user = User()
    user.surname = 'Scott'
    user.name = 'Ridley'
    user.age = '21'
    user.position = 'captain'
    user.address = 'module_1'
    user.email = 'scott_chief@mars.org'
    db_sess.add(user)
    db_sess.commit()
    ###################################
    user = User()
    user.surname = 'Danielson'
    user.name = 'Daniel'
    user.age = '15'
    user.position = 'worker'
    user.address = 'module_2'
    user.email = 'daniel_15@mars.org'
    db_sess.add(user)
    db_sess.commit()
    ###################################
    user = User()
    user.surname = 'Glebovich'
    user.name = 'Gleb'
    user.age = '25'
    user.position = 'engineer'
    user.address = 'module_3'
    user.email = 'glebrus@mars.org'
    db_sess.add(user)
    db_sess.commit()
    ###################################
    user = User()
    user.surname = 'Ryan'
    user.name = 'Gosling'
    user.age = '41'
    user.position = 'driver'
    user.address = 'module_4'
    user.email = 'ryan_gosling_cool@mars.org'
    db_sess.add(user)
    db_sess.commit()
    ######################################
    job = Jobs()
    job.team_leader = 1
    job.job = "deployment of residential modules 1 and 2"
    job.work_size = 15
    job.collaborators = "2, 3"
    job.is_finished = False
    db_sess.add(job)
    db_sess.commit()
    ######################################
    job = Jobs()
    job.team_leader = 3
    job.job = "minerals research"
    job.work_size = 20
    job.collaborators = "1"
    job.is_finished = False
    db_sess.add(job)
    db_sess.commit()
    ######################################
    job = Jobs()
    job.team_leader = 4
    job.job = "driving ouuta here"
    job.work_size = 10
    job.collaborators = "2"
    job.is_finished = False
    db_sess.add(job)
    db_sess.commit()
    ######################################

@app.route('/')
@app.route('/index')
def index():
    params = {
        'title': 'Лист с профессиями',
        'navbar_title': 'Миссия Колонизация Марса',
        'list_type': list_type,
        'prof_list': ['инженер-исследователь', 'пилот', 'строитель', 'экзобиолон', 'врач',
                      'инжинер по терраформированию', 'климатоллог'],
        'hrefs': return_links()
    }
    return render_template('list_prof.html', **params)


if __name__ == '__main__':
    main()
