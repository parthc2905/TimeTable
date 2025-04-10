from flask import render_template,redirect,url_for,request,session,jsonify
from TimeTable.index import tableGen
from TimeTable import app
from TimeTable.models import User,Student,Faculty,Admin,Task
from TimeTable.forms import RegisterForm,InputDetail,StudentInfo,FacultyInfo,AdminInfo,LoginDetail,TaskDetail,RemoveTaskDetail
from TimeTable import db
import json,os,datetime

@app.route("/",methods=['GET','POST'])
@app.route("/home", methods=['GET','POST'])
def home_page():
    if request.method == "POST":
        if request.form["submit"] == "Generate":
            return redirect(url_for('input_page'))
        else:
            return redirect(url_for('view_page'))
    return render_template('home.html')
    
@app.route("/Input",methods=['GET','POST'])
def input_page():
    form = InputDetail()
    if form.validate_on_submit():
        faculty = form.facultyName.data.split(',')
        subject = form.subjects.data.split(',')
        division,day,lecTime,lecBlock = tableGen(form.daysPerWeek.data,form.numberOfLec.data,form.numberOfSub.data,form.breakTime.data,faculty,subject,form.lectureDuration.data,form.numberOfdiv.data)
        days = ["Time","Mon", "Tue", 'Wed', 'Thu', 'Fri', 'Sat']
        store = {}
        store['div'] = division
        store['extra'] = [day,lecTime,lecBlock]
        with open('table.json','w+') as file:
            if os.path.exists('table.json') and os.path.getsize('table.json') > 0:
                os.remove('table.json')
            
            json.dump(store,file)

        return render_template("log.html",d=division,weeks=day,sizes=lecTime,block=lecBlock,days=days)

    return render_template('input.html',form=form)

@app.route("/View")
def view_page():
    with open('table.json' , 'r+') as file:
        data = json.load(file)
    days = ["Time","Mon", "Tue", 'Wed', 'Thu', 'Fri', 'Sat']
    return render_template("log.html",d=data['div'],weeks=data['extra'][0],sizes=data['extra'][1],block=data['extra'][2],days=days)


@app.route("/dashboard",methods=['GET','POST'])
def dashboard_page():
    # event = ['2025-04-16', '2025-04-03', '2025-04-10']'
    tasks = Task.query.filter_by(own=2).all()
    event = [str(task.event_date) for task in tasks]
    date_events = {}
    for i in tasks:
        date_events[i.event_date] = i.description 
    return render_template('calender.html',event=event,tasks=tasks,date_events=date_events)

@app.route("/task",methods=['GET','POST'])
def task_page():
    task = TaskDetail()
    # if request.method == 'POST':
    #     print(task.errors)
    tasks = Task.query.filter_by(own=2).all()
    if task.validate_on_submit():
        user_input = str(task.date.data)
        desc = task.desc.data
        parsed_date = datetime.datetime.strptime(user_input, "%Y-%m-%d").date()

        # print(user_input,desc,type(parsed_date))
        task_to_create = Task(event_date=parsed_date,
                     description=desc,
                     own=session.get('student_id')
                     )
        db.session.add(task_to_create)
        db.session.commit()

    return render_template('task.html',task=task,tasks=tasks)

@app.route('/removetask',methods=['GET','POST'])
def remove_task_page():
    tasks = Task.query.filter_by(own=2).all()
    task = RemoveTaskDetail()

    if task.validate_on_submit():
        if task.select.data <= len(tasks):
            task_num = task.select.data
            taskk = Task.query.filter_by(description=tasks[task_num-1].description).first()
            db.session.delete(taskk)
            db.session.commit()
        else:
            print("No task to remove")
    return render_template('removetask.html',tasks=tasks,task=task)

@app.route("/studentinfo", methods=['GET','POST'])
def student_info():
    form1 = StudentInfo()
    userid = request.args.get('userid')
    user = User.query.get(int(userid))
    if form1.validate_on_submit():
        student_to_create = Student(enroll=form1.enroll.data,
                                    name=form1.name.data,
                                    sem=form1.sem.data,
                                    mentorid=form1.mentor.data,
                                    owner=user
                                    )
        db.session.add(student_to_create)
        db.session.commit()
        id = student_to_create.id
        return redirect(url_for('dashboard_page',studentid=id))
    return render_template('studentinfo.html',form1=form1)



@app.route('/facultyinfo', methods=['GET','POST'])
def faculty_info(): 
    form2 = FacultyInfo()
    factyid = request.args.get('factyid')
    facty = User.query.get(int(factyid))
    if form2.validate_on_submit():
        faculty_to_create = Faculty(facultyId=form2.facultyid.data,
                                    name=form2.name.data,
                                    owner=facty
                                    )
        db.session.add(faculty_to_create)
        db.session.commit()
        return redirect(url_for('home_page'))
    return render_template('facultyinfo.html',form2=form2)


@app.route('/admininfo', methods=['GET','POST'])
def admin_info():
    form3 = AdminInfo()
    adminid = request.args.get('adminid')
    adm = User.query.get(int(adminid))
    if form3.validate_on_submit():
        admin_to_create = Admin(adminId=form3.adminId.data,
                                    orgId=form3.orgId.data,
                                    orgname=form3.orgName.data,
                                    contact=form3.contactDetails.data,
                                    owner=adm
                                    )
        db.session.add(admin_to_create)
        db.session.commit()
        return redirect(url_for('home_page'))
    return render_template('adminInfo.html',form3=form3)


@app.route("/register", methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create  = User(username=form.username.data,
                               email=form.email.data,
                               password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        id = user_to_create.id
        if form.username.data == '1':
            session['student_id'] = id
            return redirect(url_for('student_info', userid=id))
        elif form.username.data == '2':
            return redirect(url_for('faculty_info',factyid=id))
        elif form.username.data == '3':
            return redirect(url_for('admin_info', adminid=id))
    return render_template('register.html',form=form)


@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginDetail()
    if form.validate_on_submit():
        user = form.username.data
        email = form.email.data
        passwd = form.password.data
        # print(user,email,passwd)
        return redirect(url_for('home_page'))
    return render_template('login.html',form=form)