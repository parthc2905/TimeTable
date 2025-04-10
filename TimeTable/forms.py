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

class RemoveTaskDetail(FlaskForm):
    select = IntegerField(label="Enter number from first to remove: ")
    submit = SubmitField(label='Remove')