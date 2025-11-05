from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db=SQLAlchemy(app)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String(200), nullable=False, unique=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200))

class Course(db.Model):
    courses={'course_1':1, 'course_2':2, 'course_3':3, 'course_4':4 }
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String(200), nullable=False, unique=True)
    course_name = db.Column(db.String(200), nullable=False)
    course_description = db.Column(db.String(200))

class Enrollments(db.Model):
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)


#change this late to app.push
"""
with app.app_context():
    db.create_all()
"""

app.app_context().push()


@app.route('/', methods=['GET', 'POST'])
def home():
    students=Student.query.all()
    return render_template('home.html', students = students)


#ADD
@app.route('/student/create', methods=['GET','POST'])
def add():
    if request.method=='GET':
        return render_template('add_student.html')
    
    elif request.method=='POST':
        roll = request.form.get('roll')
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name') #get is for fetching 1 entry 
        scourse = request.form.getlist('courses') #getlist of for fetching all the courses that the checkbox is ticked for
        exist=Student.query.filter_by(roll_number=roll).first() #roll_number is from db & roll is from thr form
        if exist is None:
            db.session.add(Student(roll_number=roll,first_name=f_name,last_name=l_name)) #student_id is auto implemented 
            db.session.commit() #to commit changes to the db and not just pythons cache memory
            courses = request.form.getlist('courses')
            for course in courses:
                db.session.add(Enrollments(estudent_id = Student.query.filter_by(roll_number=roll).first().student_id,
                                           ecourse_id = Course.courses[course]))
                db.session.commit()
            
            return redirect('/')
        return render_template('exists.html')




#UPDATE
@app.route('/student/<int:student_id>/update', methods=['GET','POST'])
def update(student_id):
    if request.method=='GET':
        row=Student.query.filter_by(student_id=student_id).first() #LHS = passing in route, RHS = in db
        enrolls=Enrollments.query.filter_by(estudent_id=student_id).all() #all because a single student can be registered to multiple courses
        cid=[enroll.ecourse_id for enroll in enrolls]
        return render_template('update.html', row=row, cid=cid)
    
    elif request.method == 'POST':
        stud = Student.query.filter_by(student_id=student_id).first()
        stud.first_name = request.form['f_name']
        stud.last_name = request.form['l_name']
        Enrollments.query.filter_by(estudent_id=student_id).delete()
        for course in request.form.getlist('courses'):
            db.session.add(Enrollments(estudent_id=student_id, ecourse_id=Course.courses[course]))
        db.session.commit()
        return redirect('/')





#DELETE
@app.route('/student/<int:student_id>/delete', methods=['GET', 'POST'])
def delete(student_id):
    Student.query.filter_by(student_id=student_id).delete()
    Enrollments.query.filter_by(estudent_id=student_id).delete()
    db.session.commit()
    return redirect('/')




#VIEW
@app.route('/student/<int:student_id>',methods=['GET', 'POST'])
def view(student_id):
    details_s = Student.query.filter_by(student_id=student_id).first()
    enrollment = Enrollments.query.filter_by(estudent_id = student_id).all()
    courses = []
    for enroll in enrollment:
        course = Course.query.filter_by(course_id=enroll.ecouse_id).first()
        if course:
            courses.append(course)
    return render_template('view.html', student=details_s, courses=courses)



if __name__ == '__main__':
    app.run(debug=True)

