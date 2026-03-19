from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

FILE = "Students.txt"


def read_students():
    students = []
    try:
        with open(FILE, "r") as f:
            for line in f:
                name, age, grade = line.strip().split(",")
                students.append({"name": name, "age": age, "grade": grade})
    except FileNotFoundError:
        pass
    return students


def write_students(students):
    with open(FILE, "w") as f:
        for s in students:
            f.write(f"{s['name']},{s['age']},{s['grade']}\n")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        grade = request.form["grade"]

        students = read_students()

        # duplicate check
        for s in students:
            if s["name"].lower() == name.lower():
                return render_template("add.html", message="Student already exists!")

        students.append({"name": name, "age": age, "grade": grade})
        write_students(students)
        return render_template("add.html", message="Student added successfully!")

    return render_template("add.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    student = None
    searched = False

    if request.method == "POST":
        name = request.form["name"]
        students = read_students()
        searched = True

        for s in students:
            if s["name"].lower() == name.lower():
                student = s
                break

    return render_template("search.html", student=student, searched=searched)


@app.route("/view")
def view():
    students = read_students()
    return render_template("view.html", students=students)


@app.route("/delete", methods=["GET", "POST"])
def delete():
    message = None
    if request.method == "POST":
        name = request.form["name"]
        students = read_students()

        new_students = [s for s in students if s["name"].lower() != name.lower()]

        if len(new_students) == len(students):
            message = "Student not found!"
        else:
            write_students(new_students)
            message = "Student deleted successfully!"

    return render_template("delete.html", message=message)


@app.route("/delete_entry/<name>", methods=["POST"])
def delete_entry(name):
    students = read_students()
    new_students = [s for s in students if s["name"].lower() != name.lower()]
    write_students(new_students)
    return redirect(url_for("view"))


if __name__ == "__main__":
    app.run(debug=True)