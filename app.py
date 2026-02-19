from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "secret123"

FILE = "students.txt"


def get_students():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        lines = f.readlines()
        return [line.strip().split(",") for line in lines]


def save_students(students):
    with open(FILE, "w") as f:
        for s in students:
            f.write(",".join(s) + "\n")


@app.route("/")
def home():
    students = get_students()
    return render_template("index.html", students=students)


@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"].strip()
        age = request.form["age"].strip()
        grade = request.form["grade"].strip()

        if not name or not age.isdigit() or not grade:
            flash("Invalid input! Please enter valid details.")
            return redirect(url_for("add_student"))

        age = int(age)
        if age <= 0 or age > 120:
            flash("Please enter a valid age.")
            return redirect(url_for("add_student"))

        students = get_students()

        # duplicate check
        for s in students:
            if s[0].lower() == name.lower():
                flash("Student already exists!")
                return redirect(url_for("home"))

        students.append([name, str(age), grade])
        save_students(students)
        flash("Student added successfully!")
        return redirect(url_for("home"))

    return render_template("add.html")


@app.route("/search", methods=["GET", "POST"])
def search_student():
    result = None
    if request.method == "POST":
        name = request.form["name"].strip()
        students = get_students()

        for s in students:
            if s[0].lower() == name.lower():
                result = s
                break

        if not result:
            flash("Student not found!")

    return render_template("search.html", student=result)


@app.route("/delete/<int:index>")
def delete_student(index):
    students = get_students()

    if 0 <= index < len(students):
        students.pop(index)
        save_students(students)
        flash("Student deleted successfully!")
    else:
        flash("Invalid student!")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
