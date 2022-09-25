import numpy as np
import pandas as pd
import os
from flask import Flask, render_template, redirect, request
import sqlite3
from AI.model import Ai

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
    #langs = request.form["langs"]
    driver_license = request.form["driverlicense"]
    subway = request.form["subway"]
    skills = request.form["skills"]
    employment = request.form["employment"]
    shedule = request.form["shedule"]
    candidate_region = request.form["candidateregion"]
    #date_created = request.form["datecreated"]
    job_id = request.form["jobid"]
    #candidate_status_id = request.form["candidatestatusid"]
    #status = request.form["status"]
    university = request.form["university"]
    faculty = request.form["faculty"]
    #graduateyear = request.form["graduateyear"]
    position = request.form["position"]
    fromyear = request.form["fromyear"]
    toyear = request.form["toyear"]
    ai = Ai()
    ai.predict()

    l = ['sex_1', 'sex_2', 'citiz_other', 'citiz_rf', 'lang_other', 'lang_rus', 'dl_A', 'dl_B', 'dl_C', 'dl_D',
     'graf_1_Change', 'graf_1_Full', 'graf_1_Look-out', 'graf_1_Not full', 'graf_1_Part', 'graf_1_does not matter',
     'graf_2_Flex', 'graf_2_Full', 'graf_2_Project', 'graf_2_Stage', 'graf_2_Volunteering', 'graf_2_does not matter',
     'age', 'salary', 'educ_col', 'educ_other', 'educ_sch', 'educ_univ', 'drive', 'mech', 'job_B', 'job_C', 'job_D',
     'same_region', 'id', 'job_id']
    data = [0]*len(l)

    df = pd.DataFrame(data, columns=l)
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM data_jobs WHERE id={job_id}")
    work = cursor.fetchone()

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
