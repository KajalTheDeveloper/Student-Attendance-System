# from flask import Flask, render_template, request, redirect
# import mysql.connector

# app = Flask(__name__)

# # Database connection
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="Kajal@887760",
#     database="user"
# )
# cursor = db.cursor()

# @app.route("/")
# def index():
#     # Fetch data for students and attendance
#     cursor.execute("SELECT * FROM students")
#     students = cursor.fetchall()

#     cursor.execute("SELECT * FROM attendance")
#     attendance = cursor.fetchall()

#     return render_template("index.html", students=students, attendance=attendance)

# @app.route("/add_student", methods=["POST"])
# def add_student():
#     name = request.form["name"]
#     student_class = request.form["class"]

#     cursor.execute("INSERT INTO students (name, class) VALUES (%s, %s)", (name, student_class))
#     db.commit()
#     return redirect("/")

# @app.route("/add_attendance", methods=["POST"])
# def add_attendance():
#     student_id = request.form["student_id"]
#     attendance_date = request.form["attendance_date"]
#     status = request.form["status"]

#     cursor.execute(
#         "INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)",
#         (student_id, attendance_date, status)
#     )
#     db.commit()
#     return redirect("/")

# @app.route("/filter", methods=["POST"])
# def filter_data():
#     table = request.form["table"]
#     column = request.form["column"]
#     operator = request.form["operator"]
#     value = request.form["value"]

#     query = f"SELECT * FROM {table} WHERE {column} {operator} %s"
#     cursor.execute(query, (value,))
#     filtered_data = cursor.fetchall()

#     # Fetch all data for rendering
#     cursor.execute("SELECT * FROM students")
#     students = cursor.fetchall()

#     cursor.execute("SELECT * FROM attendance")
#     attendance = cursor.fetchall()

#     return render_template("index.html", students=students, attendance=attendance, filtered_data=filtered_data)

# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Kajal@887760",
    database="user"
)
cursor = db.cursor()

@app.route("/")
def index():
    # Fetch data for students and attendance
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.execute("SELECT * FROM attendance")
    attendance = cursor.fetchall()

    return render_template("index.html", students=students, attendance=attendance)

@app.route("/add_student", methods=["POST"])
def add_student():
    name = request.form["name"]
    student_class = request.form["class"]

    cursor.execute("INSERT INTO students (name, class) VALUES (%s, %s)", (name, student_class))
    db.commit()
    return redirect("/")

@app.route("/add_attendance", methods=["POST"])
def add_attendance():
    student_id = request.form["student_id"]
    attendance_date = request.form["attendance_date"]
    status = request.form["status"]

    cursor.execute(
        "INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)",
        (student_id, attendance_date, status)
    )
    db.commit()
    return redirect("/")

@app.route("/query", methods=["POST"])
def query():
    operator_type = request.form["operator_type"]
    query_result = None

    # Examples of various SQL operators
    if operator_type == "in":
        cursor.execute("SELECT * FROM students WHERE class IN ('10A', '10B')")
        query_result = cursor.fetchall()
    elif operator_type == "not_in":
        cursor.execute("SELECT * FROM students WHERE class NOT IN ('10A', '10B')")
        query_result = cursor.fetchall()
    elif operator_type == "between":
        cursor.execute("SELECT * FROM attendance WHERE student_id BETWEEN 1 AND 5")
        query_result = cursor.fetchall()
    elif operator_type == "like":
        cursor.execute("SELECT * FROM students WHERE name LIKE 'A%'")
        query_result = cursor.fetchall()
    elif operator_type == "exists":
        cursor.execute("""
            SELECT * FROM students WHERE EXISTS (
                SELECT 1 FROM attendance WHERE students.id = attendance.student_id
            )
        """)
        query_result = cursor.fetchall()
    elif operator_type == "any":
        cursor.execute("""
            SELECT * FROM attendance WHERE status = ANY (SELECT DISTINCT status FROM attendance)
        """)
        query_result = cursor.fetchall()
    elif operator_type == "some":
        cursor.execute("""
            SELECT * FROM attendance WHERE status = SOME (SELECT DISTINCT status FROM attendance)
        """)
        query_result = cursor.fetchall()

    # Fetch all data for rendering
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.execute("SELECT * FROM attendance")
    attendance = cursor.fetchall()

    return render_template(
        "index.html", 
        students=students, 
        attendance=attendance, 
        query_result=query_result,
        operator_type=operator_type
    )

if __name__ == "__main__":
    app.run(debug=True)

