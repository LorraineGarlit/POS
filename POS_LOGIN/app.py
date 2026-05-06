from flask import Flask, render_template, request, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = "secret123"

# -----------------------
# LOAD USERS
# -----------------------
def load_users():
    if not os.path.exists("users.json"):
        return []
    with open("users.json", "r") as f:
        return json.load(f)

# -----------------------
# SAVE USERS
# -----------------------
def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

# -----------------------
# LOGIN PAGE
# -----------------------
@app.route("/")
def home():
    return render_template("index.html")

# -----------------------
# LOGIN PROCESS
# -----------------------
@app.route("/login", methods=["POST"])
def login():
    users = load_users()

    username = request.form["username"]
    password = request.form["password"]

    for user in users:
        if user["username"] == username and user["password"] == password:
            session["user"] = username
            return redirect("/dashboard")

    return "Invalid username or password"

# -----------------------
# REGISTER PAGE
# -----------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users = load_users()

        new_user = {
            "username": request.form["username"],
            "password": request.form["password"],
            "email": request.form["email"]
        }

        # check duplicate username
        for user in users:
            if user["username"] == new_user["username"]:
                return "Username already exists"

        users.append(new_user)
        save_users(users)

        return redirect("/")  # back to login

    return render_template("register.html")

# -----------------------
# FORGOT PASSWORD
# -----------------------
@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        email = request.form["email"]
        users = load_users()

        for user in users:
            if user.get("email") == email:
                return "Reset link sent (demo only)"

        return "Email not found"

    return render_template("forgot.html")

# -----------------------
# DASHBOARD (PROTECTED)
# -----------------------
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", user=session["user"])
    return redirect("/")

# -----------------------
# LOGOUT
# -----------------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# -----------------------
# RUN APP
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)