from flask import Flask, jsonify, render_template, url_for, redirect, request, session
from pymongo import MongoClient
from os import environ
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="static")

app.secret_key = environ["SECRET_KEY"]

try:
    client = MongoClient(environ["MONGO_URI"])
    db = client["todo-list"]
    todos = db["todos"]
    user_ids = db["user ids"]

    print("Connected to MongoDB successfully!")
except Exception as E:
    print(f"Error while connecting: {E}")

@app.route("/")
def home():
    if session.get("USER_ID"):
        return render_template("home.html")
    else:
        return redirect(url_for("signup"))

@app.route("/todos/get/<int:user_id>")
def get_todos(user_id):
    user_todos = [todo for todo in todos.find({"user_id": user_id}, {"_id": 0})]

    return jsonify(user_todos)

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        get_id = request.form.get("user_id")

        if (user_ids.find_one({"user_id":  get_id})):
            return render_template("signup.html", already_exists = True)
        else:
            user_ids.insert_one({"user_id": get_id})
            session["USER_ID"] = get_id
            return redirect(url_for("home"))

@app.route("/todos/create", methods = ["POST"])
def create_todo():
    new_todo = {
        # "user_id": session["USER_ID"],
        "user_id": 64,
        "title": request.args.get("title"),
        "description": request.args.get("description")
    }

    try:
        todos.insert_one(new_todo)
        return "Success"
    except Exception as E:
        return f"Error: {E}"

if __name__ == '__main__':
    app.run(debug=True)
