import os
import time
import argparse
import logging
from time import sleep
from multiprocessing import Process, Queue
from flask import jsonify, request, Flask
from flaskext.mysql import MySQL


app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("db_root_password")
app.config["MYSQL_DATABASE_DB"] = os.getenv("db_name")
app.config["MYSQL_DATABASE_HOST"] = os.getenv("MYSQL_SERVICE_HOST")
app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("MYSQL_SERVICE_PORT"))
mysql.init_app(app)


@app.route("/")
def index():
    sql = "SELECT COUNT(*) FROM jobs"
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        count = results[0][0]
        cursor.close()
        conn.close()
        resp = jsonify(f"Current succesful job count is {count}")
        resp.status_code = 200
        return resp
    except Exception as e:
        return jsonify(str(e))


@app.route("/job", methods=["POST"])
def add_user():
    json = request.json
    job_time_s = json["timeSeconds"]
    eval_time = json["evaluationTime"]
    start_time = json["startTime"]
    if job_time_s and request.method == "POST":
        sleep(float(job_time_s))
        if time.time() - start_time < eval_time:
            return jsonify("Job surpassed evaluation time")
        sql = "INSERT INTO jobs VALUES ()"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return jsonify("Job submitted")

    else:
        return jsonify("Please provide job time")


@app.route("/clear", methods=["POST"])
def clear_jobs_table():
    if request.method == "POST":
        sql = "DELETE FROM jobs"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return jsonify("Jobs table cleared")

    else:
        return jsonify("Something went wrong")


if __name__ == "__main__":
    # Threaded off because each pod represents job
    app.run(host="0.0.0.0", port=5000, threaded=False)
