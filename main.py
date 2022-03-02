import sqlalchemy

from data import db_session
from data.users import User
from data.jobs import Jobs

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    # app.run()
    db_sess = db_session.create_session()
    ####################################
    # user = User()
    # user.surname = 'Scott'
    # user.name = 'Ridley'
    # user.age = '21'
    # user.position = 'captain'
    # user.address = 'module_1'
    # user.email = 'scott_chief@mars.org'
    # db_sess.add(user)
    # db_sess.commit()
    ######################################
    job = Jobs()
    job.team_leader = 1
    job.job = "deployment of residential modules 1 and 2"
    job.work_size = 15
    job.collaborators = "2, 3"
    job.is_finished = False
    db_sess.add(job)
    db_sess.commit()

if __name__ == '__main__':
    main()
