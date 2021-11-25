from flask import Flask, request

from flask_cors import CORS
import mysql.connector
import json
app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
    host="localhost", user="root", passwd="", database="todoapp")


@app.route("/auth", methods=['POST'])
def auth():
    data = request.get_json()
    username = data['username']
    password = data['password']

    cursor = db.cursor()

    check_user_stmt = "SELECT name FROM users WHERE name = '" + username+"'"

    insrt_stmt = "INSERT INTO users(name, password) VALUES(%s, %s)"
    data = (username, password)

    check_credential_stmt = "SELECT name, password FROM users WHERE name = '" + \
        username+"' and password='"+password+"'"

    try:
        cursor.execute(check_user_stmt)
        res = cursor.fetchall()
        if res:
            cursor.execute(check_credential_stmt)
            res2 = cursor.fetchall()
            if(res2):
                return json.dumps({
                    "status": True,
                })
            else:
                return json.dumps({
                    "status": False,
                    "error": "Invalid credentials, Try Again"
                })
        else:
            cursor.execute(insrt_stmt, data)
            db.commit()
            return json.dumps({
                "status": True,
            })
    except:
        return json.dumps({
            "status": False,
            "error": "Something Went Wrong, Try Again"
        })


@app.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    username = data["username"]
    greet = data["greet"]
    cursor = db.cursor()
    stmt = "INSERT INTO tasks(name, task) VALUES(%s, %s)"
    data = (username, greet)

    try:
        cursor.execute(stmt, data)
        db.commit()
        return json.dumps({
            "status": True,
        })
    except:
        return json.dumps({
            "status": False,
            "error": "Couldn't create task, Try Again"
        })


@app.route("/list", methods=["POST"])
def listAll():
    def transform(x):
        return {
            'task': x[0],
            'taskid': x[1]
        }
    data = request.get_json()
    username = data["username"]
    cursor = db.cursor()

    stmt = "SELECT task, taskid FROM tasks WHERE name='" + username+"'"

    try:
        cursor.execute(stmt)
        res = cursor.fetchall()
        return json.dumps({
            "status": True,
            "data": list(map(transform, res))
        })
    except Exception as e:
        return json.dumps({
            "status": False,
            "error": "Something went wrong, Try Again"
        })


@app.route("/delete", methods=["DELETE"])
def delete():
    data = request.get_json()
    taskid = data["id"]
    print(type(taskid))
    cursor = db.cursor()

    stmt = "DELETE FROM tasks WHERE taskid= {}".format(taskid)

    try:
        res = cursor.execute(stmt)
        db.commit()
        return json.dumps({
            "status": True,
            "data": res
        })
    except Exception as e:
        return json.dumps({
            "status": False,
            "error": "Something Went Wrong, try again"
        })


if __name__ == "__main__":
    app.run()
