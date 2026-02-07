from flask import Flask, render_template, request, redirect, session
from database.db_connection import get_connection

app = Flask(__name__)
app.secret_key = "career123"

def predict_career(stream, percentage, interest, coding):
    if stream == "Science" and coding >= 7:
        return "Software Developer"
    elif stream == "Commerce" and percentage > 70:
        return "Chartered Accountant"
    elif stream == "Arts" and "design" in interest.lower():
        return "Graphic Designer"
    else:
        return "Career Counselor Recommended"

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students(full_name,email,password,phone) VALUES (?,?,?,?)",
            (name,email,password,phone)
        )
        conn.commit()
        return redirect("/")
    return render_template("signup.html")

@app.route("/dashboard", methods=["POST"])
def dashboard():
    email = request.form["email"]
    password = request.form["password"]

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT student_id FROM students WHERE email=? AND password=?",
                (email,password))
    row = cur.fetchone()

    if row:
        session["sid"] = row[0]
        return redirect("/profile")
    return "Invalid Login"

@app.route("/profile", methods=["GET","POST"])
def profile():
    if request.method == "POST":
        stream = request.form["stream"]
        percent = float(request.form["percent"])
        interest = request.form["interest"]
        subject = request.form["subject"]
        coding = int(request.form["coding"])

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO student_profile VALUES (?,?,?,?,?,?)",
            (session["sid"], stream, percent, interest, subject, coding)
        )
        conn.commit()

        result = predict_career(stream, percent, interest, coding)
        return render_template("result.html", career=result)

    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)
