from crypt import methods
import os
from flask import Flask, render_template, redirect, request
import sqlite3

DATABASE = "/tmp/AISorter.db"
DEBUG = True
SECRET_KEY = "veq7rcm3136bcr4310vb6x32zfhvbwk"

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, "../DataBase/AISorter.db")))


@app.route("/")
def index():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM data_jobs")
    total_rows = cursor.fetchall()
    return render_template("index.html", total_rows=total_rows)

@app.route("/conclusion/", methods=["POST"])
def conclusion():
    
    sex = request.form["sex"]
    citizenship = request.form["citizenship"]
    age = request.form["age"]
    salary = request.form["salary"]
    langs = request.form["langs"]
    driver_license = request.form["driverlicense"]
    subway = request.form["subway"]
    skills = request.form["skills"]
    employment = request.form["employment"]
    shedule = request.form["shedule"]
    candidate_region = request.form["candidateregion"]
    date_created = request.form["datecreated"]
    job_id = request.form["jobid"]
    candidate_status_id = request.form["candidatestatusid"]
    status = request.form["status"]

    return "<h1>0.98</h1>"

@app.route("/work/<work_id>")
def work(work_id):
    db = connect_db()
    cursor = db.cursor()
    if work_id.isdigit():
        cursor.execute(f"SELECT * FROM data_jobs WHERE id={work_id}")
        work = cursor.fetchone()
    else:
        work = None

    if work != None:
        return render_template("work.html", work=work)
    return redirect("/")


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
