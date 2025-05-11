from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField, SubmitField, SelectField, IntegerField, DateField

class RegisterForm(FlaskForm):
    username = SelectField(choices = [('1','Student'),('2','Faculty'),('3','Admin')], default = ['1'],label='User :')
    email = StringField(label='Email: ')
    password1 = PasswordField(label='Password: ')
    password2 = PasswordField(label='Confirm Password: ')
    submit = SubmitField(label='Create Account')

class StudentInfo(FlaskForm):
    enroll = IntegerField(label="Enter Enrollment number :")
    name = StringField(label="Enter name as per GTU marksheet: ")
    sem = SelectField(choices=[(1,'1st sem'),(2,'2nd sem'),(3,'3rd sem'),(4,'4th sem'),(5,'5th sem'),(6,'6th sem'),(7,'7th sem'),(8,'8th sem')],default=['1'],label="Semester :")
    mentor = StringField(label="Enter Mentor ID: ")
    submit = SubmitField(label='Submit')


class FacultyInfo(FlaskForm):
    facultyid = IntegerField(label="Enter Faculty ID :")
    name = StringField(label="Enter name : ")
    submit = SubmitField(label='Submit')

class AdminInfo(FlaskForm):
    adminId = IntegerField(label="Enter Admin Id : ")
    orgId = IntegerField(label="Enter Organization/college Code: ")
    orgName = StringField(label="Enter Organization/college Name: ")
    contactDetails = StringField(label="Enter Contact for oraganization: ")
    submit = SubmitField(label='Submit')


class InputDetail(FlaskForm):
    numberOfSub = IntegerField(label='Enter Number of Subjects: ')
    numberOfLec = IntegerField(label='Enter Number of Lectures per day: ')
    breakTime = IntegerField(label='Enter Break Time(in minutes): ')
    numberOfdiv = IntegerField(label='Enter Number of Divisions : ')
    lectureDuration = IntegerField(label='Enter Duration of a Lecture(in minutes) : ')
    facultyName = StringField(label="Enter Names of faculty (separate by comma  i.e.',') :")
    subjects = StringField(label="Enter Subjects (same order as per faculty and separate by comma i.e.',') :")
    daysPerWeek = IntegerField(label='Enter Number of Days per Week: ')
    submit = SubmitField(label='Generate Schedule')


class LoginDetail(FlaskForm):
    username = SelectField(choices = [('1','Student'),('2','Faculty'),('3','Admin')], default = ['1'],label='User :')
    email = StringField(label='Email: ')
    password = PasswordField(label='Password: ')
    submit = SubmitField(label='Login')


class TaskDetail(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d')
    desc = StringField(label='Task Description : ')
    submit = SubmitField(label='Task')


class ViewDetail(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d')
    submit = SubmitField(label='Task')

class RemoveTaskDetail(FlaskForm):
    select = IntegerField(label="Enter number from first to remove: ")
    submit = SubmitField(label='Remove')

class AdminStudent(FlaskForm):
    choose = SelectField(choices = [('1','Add Student'),('2','Remove Student')], default = ['1'],label='Add/Delete :')
    enroll = IntegerField(label="Enter Enrollment number :")
    name = StringField(label="Enter name as per GTU marksheet: ")
    email = StringField(label='Email: ')
    password = PasswordField(label='Password: ')
    sem =    SelectField(choices=[(1,'1st sem'),(2,'2nd sem'),(3,'3rd sem'),(4,'4th sem'),(5,'5th sem'),(6,'6th sem'),(7,'7th sem'),(8,'8th sem')],default=['1'],label="Semester :")
    mentor = StringField(label="Enter Mentor ID: ")
    submit = SubmitField(label='Add/Remove')

class AdminFaculty(FlaskForm):
    choose = SelectField(choices = [('1','Add Faculty'),('2','Remove Faculty')], default = ['1'],label='Add/Delete :')
    facultyid = IntegerField(label="Enter Faculty ID :")
    name = StringField(label="Enter name : ")
    email = StringField(label='Email: ')
    password = PasswordField(label='Password: ')
    submit = SubmitField(label='Add/Remove')

class AdminBranchDivision(FlaskForm):
    choose = SelectField(choices = [('1','Add Branch'),('2','Remove Branch')], default = ['1'],label='Add/Delete :')
    branch = StringField(label="Enter Branch: ")
    division = IntegerField(label="Enter number of Division: ")
    submit = SubmitField(label='Add/Remove')

class AdminCourse(FlaskForm):
    choose = SelectField(choices = [('1','Add Course'),('2','Remove Course')], default = ['1'],label='Add/Delete :')
    courseid = IntegerField(label="Enter Course ID :")
    name = StringField(label="Enter Course Name : ")
    submit = SubmitField(label='Add/Remove')

class AdminClassLocation(FlaskForm):
    choose = SelectField(choices = [('1','Add Class Location'),('2','Remove Class Location')], default = ['1'],label='Add/Delete :')
    classLocation = StringField(label="Enter Class Location (e.g. A101): ")
    floor = IntegerField(label="Enter Floor Number: ")
    submit = SubmitField(label='Add/Remove')