from TimeTable import db

class User(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(length=2),nullable=False)
    email = db.Column(db.String(length=50),nullable=False,unique=True)
    password_hash = db.Column(db.String(length=68),nullable=False)
    student = db.relationship('Student', backref="owner", uselist=False)
    faculty = db.relationship('Faculty', backref="owner", uselist=False)
    admin = db.relationship('Admin', backref="owner", uselist=False)
    
class Student(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    enroll = db.Column(db.Integer(),unique=True,nullable=False)
    name = db.Column(db.String(length=68))
    sem =  db.Column(db.Integer())
    mentorid = db.Column(db.String(length=68),nullable=False)
    own = db.Column(db.Integer(),db.ForeignKey('user.id'))
    task = db.relationship('Task', backref="owner", uselist=False)

class Faculty(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    facultyId = db.Column(db.Integer(),unique=True,nullable=False)
    name = db.Column(db.String(length=68))
    own = db.Column(db.Integer(),db.ForeignKey('user.id'))

class Admin(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    adminId = db.Column(db.Integer())
    orgId = db.Column(db.Integer(),unique=True,nullable=False)
    orgname = db.Column(db.String(length=150))
    contact = db.Column(db.String(length=10))
    own = db.Column(db.Integer(),db.ForeignKey('user.id'))

class Task(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    event_date = db.Column(db.Date())
    description = db.Column(db.String(length=60))
    own = db.Column(db.Integer(),db.ForeignKey('student.id'))
    

# class Courses(db.Model):
#     id = db.Column(db.Integer(),primary_key=True)
#     courseid = db.Column(db.Integer(),unique=True,nullable=False)
#     name = db.Column(db.String(length=68))
#     student = db.relationship('Student', backref="owner", uselist=False)

# class Locations(db.Model):
#     id = db.Column(db.Integer(),primary_key=True)
#     classLocation = db.Column(db.String(length=10),unique=True,nullable=False)
#     floor = db.Column(db.Integer(),nullable=False)
