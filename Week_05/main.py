#file not to be submitted

from app import db,Course,app

with app.app_context():

    courses = [
        Course(course_id=1, course_code="CSE01", course_name ="MAD I", course_description="Modern Application Development - I"),
        Course(course_id=2, course_code="CSE02", course_name ="DBMS", course_description="Database management Systems"),
        Course(course_id=3, course_code="CSE03", course_name ="PDSA", course_description="Programming, ata Structures and Algorithms using Python"),
        Course(course_id=4, course_code="BST13", course_name ="BDM", course_description="Business Data Managament")
    ]

    db.session.add_all(courses )
    db.session.commit()