import os
from flask import Flask, render_template
import sqlite3

DATABASE = "/tmp/AISorter.db"
DEBUG = True
SECRET_KEY = "veq7rcm3136bcr4310vb6x32zfhvbwk"

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, "../DataBase/AISorter.db")))

@app.route("/")
def hello_world():
    db = connect_db()
    #db.cursor
    db.commit()
    db.close()
    return render_template("index.html")


def connect_db():
    connection = sqlite3.connect(app.config["DATABASE"])
    connection.row_factory = sqlite3.Row
    return connection

# Creating new table
def create_table_db():      
    db = connect_db()
    with app.open_resource("/sql/__.sql", mode="r") as file:
        db.cursor().executescript(file.read())
    db.commit()
    db.close()

if __name__ == "__main__":
    app.run()

