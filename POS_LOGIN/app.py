from flask import Flask, render_template, request, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = "secret123"

def load_users():
    if not os.path.exists("users.json"):
        return []
    with open("users.json", "r") as f:
        return json.load(f)

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

@app.route("/")
def index():
    return render_template("admin_staff.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()

        for user in users:
            if user["username"] == username:
                return "Username already exists"

        users.append({
            "username": username,
            "password": password
        })

        save_users(users)
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()

        for user in users:
            if user["username"] == username and user["password"] == password:
                session["username"] = username
                return redirect("/dashboard")

        return "Invalid username or password"

    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/login")

    return render_template("dashboard.html", username=session["username"])

@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect("/login")

    return render_template("profile.html", username=session["username"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)