from main import app
from data import db_session

if __name__ == "__main__":
    db_session.global_init("./db/mars_explorer.sqlite")
    app.run()
