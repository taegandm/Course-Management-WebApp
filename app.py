import sqlparse
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from MySQLConfig import MySQLConfig

app = Flask(__name__)

# Configure MySQL using the imported config
app.config['MYSQL_HOST'] = MySQLConfig.HOST
app.config['MYSQL_USER'] = MySQLConfig.USER
app.config['MYSQL_PASSWORD'] = MySQLConfig.PASSWORD
app.config['MYSQL_DB'] = MySQLConfig.DATABASE

# Create a MySQL connection
mysql = MySQL(app)

# Dictionary to store grade values
gradeValue = {
    'A+': 4.0,
    'A': 4.0,
    'A-': 3.7,
    'B+': 3.3,
    'B': 3.0,
    'B-': 2.7,
    'C+': 2.3,
    'C': 2.0,
    'C-': 1.7,
    'D+': 1.3,
    'D': 1.0,
    'D-': 0.7,
    'F': 0
}


def execute_initial_sql(mysql):
    try:
        cursor = mysql.connection.cursor()
        # Read and execute the initial.sql file
        with open('static/sql/init.sql') as sql_file:
            statements = sqlparse.split(sql_file.read())
            for query in statements:
                print(query)
                cursor.execute(query)
                mysql.connection.commit()

        cursor.close()
    except Exception as e:
        print(f"Error executing initial SQL script: {str(e)}")


with app.app_context():
    execute_initial_sql(mysql)


# open website, load student information
@app.route('/')
def index():

    # Display a list of records from the database
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        type = request.form['type']
        path = ''
        cursor = mysql.connection.cursor()
        if int(type) == 0:
            cursor.execute("SELECT pword FROM Admin WHERE username = %s", (username,))
        elif int(type) == 1:
            cursor.execute("SELECT pword, sid FROM Student WHERE username = %s", (username,))
        savedPassword = cursor.fetchone()
        cursor.close()
        if savedPassword is None:
            return render_template("error.html", errorType="Login Error", message="Username is Incorrect",
                                   redirectLocation="Back to Login", path=path)
        elif str(password) == str(savedPassword[0]) and int(type) == 0:
            return redirect(url_for('adminHome'))
        elif str(password) == str(savedPassword[0]) and int(type) == 1:
            return redirect(url_for('studentHome', sid=savedPassword[1]))
        else:
            return render_template("error.html", errorType="Login Error", message="Password is Incorrect",
                                   redirectLocation="Back to Login", path=path)


# open website, load student information
@app.route('/adminHome')
def adminHome():

    # Display a list of records from the database
    updateGPAs()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Student")
    students = cursor.fetchall()
    cursor.execute("SELECT * FROM Course")
    courses = cursor.fetchall()
    cursor.execute("SELECT * FROM Enrolled")
    enrolled = cursor.fetchall()
    cursor.close()
    return render_template('adminHome.html', students=students, courses=courses, enrolled=enrolled)


@app.route('/studentHome/<int:sid>')
def studentHome(sid):

    # Display a list of records from the database
    updateGPAs()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Student WHERE sid = %s", (sid,))
    studentInfo = cursor.fetchall()
    cursor.execute("SELECT * FROM Course")
    courses = cursor.fetchall()
    cursor.execute("SELECT * FROM Enrolled WHERE sid = %s", (sid,))
    enrolled = cursor.fetchall()
    cursor.close()
    return render_template('studentHome.html', studentInfo=studentInfo, courses=courses, enrolled=enrolled)


# Route for adding students
@app.route('/addStudent', methods=['POST'])
def addStudent():
    if request.method == 'POST':
        sname = request.form['sname']
        username = request.form['username']
        email = request.form['email']
        pnum = request.form['pnum']
        dob = request.form['dob']
        gpa = request.form['gpa']
        pword = request.form['pword']
        path = "adminHome"
        if not checkUnique(0, username, email, pnum):
            return render_template("error.html", errorType="Update Error", message="Username, email, and phone "
                                   "number must be unique", redirectLocation="Back to Admin Home", path=path)
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Student (sname, username, email, pnum, dob, gpa, pword) VALUES ('{}', '{}', '{}', '{}', "
                       "'{}', '{}', '{}')".format(sname, username, email, pnum, dob, gpa, pword))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('adminHome'))


@app.route('/addCourse', methods=['POST'])
def addCourse():
    if request.method == 'POST':
        cname = request.form['cname']
        description = request.form['description']
        credits = request.form['credits']
        capacity = request.form['capacity']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Course (cname, description, credits, capacity) VALUES ('{}', '{}', '{}', '{}')".format(cname, description, credits, capacity))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('adminHome'))


@app.route('/enrollStudent', methods=['POST'])
def enrollStudent():
    if request.method == 'POST':
        sid = request.form['sid']
        cid = request.form['cid']
        grade = request.form['grade']
        path = "adminHome"
        if alreadyEnrolled(sid, cid):
            return render_template("error.html", errorType="Enrollment Error", message="Student is already enrolled"
                                   " in this class", redirectLocation="Back to Admin Home", path=path)
        if courseFull(cid):
            return render_template("error.html", errorType="Enrollment Error", message="This course is full",
                                   redirectLocation="Back to Admin Home", path=path)
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Enrolled (sid, cid, grade) VALUES ('{}', '{}', '{}')".format(sid, cid, grade))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('adminHome'))


# Route for deleting students
@app.route('/delete/<string:type>/<int:id>')
def delete(type, id):
    cursor = mysql.connection.cursor()
    if str(type) == 'student':
        cursor.execute("DELETE FROM Student WHERE sid = %s", (id,))
    elif str(type) == 'course':
        cursor.execute("DELETE FROM Course WHERE cid = %s", (id,))
    else:
        cursor.execute("DELETE FROM Enrolled WHERE sid = %s AND cid = %s", (type, id))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('adminHome'))


@app.route('/updateStudent/<int:sid>', methods=['GET', 'POST'])
def updateStudent(sid):
    if request.method == 'POST':
        sname = request.form['sname']
        username = request.form['username']
        email = request.form['email']
        pnum = request.form['pnum']
        dob = request.form['dob']
        gpa = request.form['gpa']
        pword = request.form['pword']
        path = "adminHome"
        if not checkUnique(sid, username, email, pnum):
            return render_template("error.html", errorType="Update Error", message="Username, email, and phone "
                                   "number must be unique", redirectLocation="Back to Admin Home", path=path)
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE Student SET sname = %s, username = %s, email = %s, pnum = %s, dob = %s, gpa = %s, "
                       "pword = %s WHERE sid = %s", (sname, username, email, pnum, dob, gpa, pword, sid))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('adminHome'))
    else:
        print(sid)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Student WHERE sid = %s", (sid,))
        result = cursor.fetchone()
        print(result)
        for row in result:
            print(row)
            # data = [row['id'], row['sname'], row['email']]
        data = result
        cursor.close()
        return render_template('updateStudent.html', data=data)


@app.route('/updateCourse/<int:cid>', methods=['GET', 'POST'])
def updateCourse(cid):
    if request.method == 'POST':
        cname = request.form['cname']
        description = request.form['description']
        credits = request.form['credits']
        capacity = request.form['capacity']
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE Course SET cname = %s, description = %s, credits = %s, capacity = %s WHERE cid = %s", (cname, description, credits, capacity, cid))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('adminHome'))
    else:
        print(cid)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Course WHERE cid = %s", (cid,))
        result = cursor.fetchone()
        print(result)
        for row in result:
            print(row)
            # data = [row['id'], row['sname'], row['email']]
        data = result
        cursor.close()
        return render_template('updateCourse.html', data=data)


@app.route('/updateEnrolled/<int:sid>/<int:cid>', methods=['GET', 'POST'])
def updateEnrolled(sid, cid):
    if request.method == 'POST':
        newSid = request.form['sid']
        newCid = request.form['cid']
        grade = request.form['grade']
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("UPDATE Enrolled SET sid = %s, cid = %s, grade = %s WHERE sid = %s AND cid = %s", (newSid, newCid, grade, sid, cid))
        except Exception as e:
            path = 'adminHome'
            return render_template("error.html", errorType="SQL Error", message=e, redirectLocation="Back to Admin Home", path=path)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('adminHome'))
    else:
        print(sid, cid)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Enrolled WHERE sid = %s AND cid = %s", (sid, cid))
        result = cursor.fetchone()
        print(result)
        for row in result:
            print(row)
            # data = [row['id'], row['sname'], row['email']]
        data = result
        cursor.close()
        return render_template('updateEnrolled.html', data=data)


def updateGPAs():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT sid FROM Student")
    student = cursor.fetchone()
    while student is not None:
        calcGPA(student)
        student = cursor.fetchone()
    cursor.close()


def calcGPA(sid):
    creditsEarned = 0
    credits = 0
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT E.grade, C.credits, C.cid FROM Course C, Enrolled E WHERE sid = %s AND E.cid = C.cid", sid)
    grade = cursor.fetchone()
    while grade is not None:
        if grade[0] == '--':
            grade = cursor.fetchone()
            continue
        if grade[0] in gradeValue:
            value = gradeValue[grade[0]] * grade[1]
            creditsEarned += value
            credits += int(grade[1])
            grade = cursor.fetchone()
        else:
            cid = grade[2]
            cursor.execute("UPDATE Enrolled SET grade = %s WHERE sid = %s AND E.cid = %s", ('--', sid, cid))
            return -1
    if credits != 0:
        cursor.execute("UPDATE Student SET gpa = %s WHERE sid = %s", (round(creditsEarned / credits, 2), sid))
    else:
        cursor.execute("UPDATE Student SET gpa = %s WHERE sid = %s", (0.00, sid))
    cursor.close()
    return 1


@app.route('/enroll/<int:sid>/<int:cid>')
def enroll(sid, cid):
    path = "studentHome/" + str(sid)
    if alreadyEnrolled(sid, cid):
        return render_template("error.html", errorType="Enrollment Error", message="You are already enrolled"
                                " in this class", redirectLocation="Back to Student Home", path=path)
    if courseFull(cid):
        return render_template("error.html", errorType="Enrollment Error",
                               message="This course is full",
                               redirectLocation="Back to Student Home", path=path)
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO Enrolled (sid, cid, grade) VALUES ('{}', '{}', '--')".format(sid, cid))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('studentHome', sid=sid))


@app.route('/drop/<int:sid>/<int:cid>')
def drop(sid, cid):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM Enrolled WHERE sid = %s AND cid = %s", (sid, cid))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('studentHome', sid=sid))


def courseFull(cid):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*), C.capacity FROM Course C, Enrolled E WHERE C.cid = E.cid AND C.cid = %s", (cid,))
    data = cursor.fetchone()
    mysql.connection.commit()
    cursor.close()
    if data[1] is None:
        return False
    numEnrolled = int(data[0])
    capacity = int(data[1])
    return numEnrolled >= capacity


def alreadyEnrolled(sid, cid):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Enrolled WHERE sid = %s AND cid = %s", (sid, cid))
    alreadyEnrolled = cursor.fetchone()
    return alreadyEnrolled is not None


def checkUnique(sid, username, email, pnum):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Student WHERE (username = %s OR email = %s OR pnum = %s) AND sid != %s",
                   (username, email, pnum, sid))
    unique = cursor.fetchone()
    return unique is None


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=9999)

