from flask import render_template,redirect,url_for,request,session,jsonify,Response,flash
from markupsafe import Markup
from TimeTable.index import tableGen
from TimeTable import app
from TimeTable.models import User,Student,Faculty,Admin,Task,BranchDivision,Courses,Locations
from TimeTable.forms import RegisterForm,InputDetail,StudentInfo,FacultyInfo,AdminInfo,LoginDetail,TaskDetail,ViewDetail,RemoveTaskDetail,AdminStudent,AdminFaculty,AdminCourse,AdminClassLocation, AdminBranchDivision
from TimeTable import db
from TimeTable.studentchatbot import StudentChatbot 
import json,os,datetime,time
from sqlalchemy import func
from markdown import markdown

chatbot = StudentChatbot(api_key="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")

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home_page():
    if request.method == "POST":
        # Check which button was clicked
        if "generate" in request.form:  # If Generate button was clicked
            return redirect(url_for('input_page'))
        elif "view" in request.form:    # If View button was clicked
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


@app.route("/chat", methods=["GET", "POST"])
def chat_page():
    if "chat_history" not in session:
        session["chat_history"] = []
        session["session_id"] = chatbot.get_new_session_id()
    
    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        if user_input:
            try:
                # Add user message to history
                session["chat_history"].append({"sender": "user", "message": user_input})
                session.modified = True
                
                # Get AI response in chunks
                response_chunks = []
                for chunk in chatbot.process_message(session["session_id"], user_input):
                    response_chunks.append(chunk)
                
                # Join chunks and format the response
                ai_response = "".join(response_chunks)
                
                # Add formatted AI response to history
                session["chat_history"].append({"sender": "ai", "message": ai_response})
                session.modified = True
                
                # Return JSON response with formatted message
                return jsonify({
                    "status": "success",
                    "user_message": user_input,
                    "ai_message": Markup(markdown(ai_response))
                })
                
            except Exception as e:
                print(f"Error processing message: {str(e)}")
                # Add error message to history
                error_message = "I'm having trouble processing your request. Please try rephrasing your question or try again later."
                session["chat_history"].append({"sender": "ai", "message": error_message})
                session.modified = True
                
                # Return error response
                return jsonify({
                    "status": "error",
                    "user_message": user_input,
                    "ai_message": Markup(markdown(error_message))
                })
    
    # Convert markdown to HTML for AI messages
    formatted_history = []
    for msg in session.get("chat_history", []):
        if msg["sender"] == "ai":
            formatted_history.append({
                "sender": msg["sender"],
                "message": Markup(markdown(msg["message"]))
            })
        else:
            formatted_history.append(msg)
    
    return render_template("studentchatbot.html", chat_history=formatted_history)



@app.route("/studentdashboard",methods=['GET','POST'])
def student_dashboard_page():
    # event = ['2025-04-16', '2025-04-03', '2025-04-10']'
    tasks = Task.query.filter_by(own=2).all()
    event = [str(task.event_date) for task in tasks]
    date_events = {}
    for i in tasks:
        date_events[i.event_date] = i.description
    return render_template('calender.html',event=event,tasks=tasks,date_events=date_events)

@app.route('/viewtask',methods=['GET','POST'])
def view_task_page():
    task = ViewDetail()
    tasks = Task.query.filter_by(own=2).all()
    if task.validate_on_submit():
        user_input = str(task.date.data)
        parsed_date = datetime.datetime.strptime(user_input, "%Y-%m-%d").date()
        tasks = Task.query.filter_by(event_date=parsed_date).all()

    return render_template('viewtask.html',task=task,tasks=tasks)

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
                     own=2
                    #  own=session.get('student_id')+
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


@app.route("/admindashboard",methods=['GET','POST'])
def admin_student():
    form = AdminStudent()
    if form.validate_on_submit():
        if form.choose.data == '1':  # Add student
            # Create new user and student
            user_to_create = User(username=1,
                                email=form.email.data,
                                password_hash=form.password.data)
    
            student_to_create = Student(enroll=form.enroll.data,
                                     name=form.name.data,
                                     sem=form.sem.data,
                                     mentorid=form.mentor.data,
                                     owner=user_to_create)
            db.session.add_all([user_to_create, student_to_create])
            db.session.commit()
            flash('Student added successfully!', 'success')
            
        elif form.choose.data == '2':  # Remove student
            # Find student by enrollment number
            student = Student.query.filter_by(enroll=form.enroll.data).first()
            if student:
                # Get the associated user
                user = student.owner
                # Delete student first (due to foreign key constraint)
                db.session.delete(student)
                # Then delete the user
                db.session.delete(user)
                db.session.commit()
                flash('Student removed successfully!', 'success')
            else:
                flash('Student not found!', 'error')
                
    # Get all students for display
    students = Student.query.all()
    return render_template('adminStudent.html', form=form, students=students)


@app.route("/adminfaculty",methods=['GET','POST'])
def admin_faculty():
    form = AdminFaculty()
    if form.validate_on_submit():
        if form.choose.data == '1':  # Add faculty
            # Create new user and faculty
            user_to_create = User(username=2,
                                email=form.email.data,
                                password_hash=form.password.data)
    
            faculty_to_create = Faculty(facultyId=form.facultyid.data,
                                     name=form.name.data,
                                     owner=user_to_create)
            db.session.add_all([user_to_create, faculty_to_create])
            db.session.commit()
            flash('Faculty added successfully!', 'success')
            
        elif form.choose.data == '2':  # Remove faculty
            # Find faculty by faculty ID
            faculty = Faculty.query.filter_by(facultyId=form.facultyid.data).first()
            if faculty:
                # Get the associated user
                user = faculty.owner
                # Delete faculty first (due to foreign key constraint)
                db.session.delete(faculty)
                # Then delete the user
                db.session.delete(user)
                db.session.commit()
                flash('Faculty removed successfully!', 'success')
            else:
                flash('Faculty not found!', 'error')
                
    # Get all faculty for display
    faculty_list = Faculty.query.all()
    return render_template('adminFaculty.html', form=form, faculty_list=faculty_list)


@app.route("/adminbranchdivision",methods=['GET','POST'])
def admin_branch_division():
    form = AdminBranchDivision()
    if form.validate_on_submit():
        if form.choose.data == '1':  # Add branch
            # Create new branch division
            branch_to_create = BranchDivision(branch=form.branch.data,
                                            division=form.division.data)
            db.session.add(branch_to_create)
            db.session.commit()
            flash('Branch added successfully!', 'success')
            
        elif form.choose.data == '2':  # Remove branch
            # Find branch by name
            branch = BranchDivision.query.filter_by(branch=form.branch.data).first()
            if branch:
                db.session.delete(branch)
                db.session.commit()
                flash('Branch removed successfully!', 'success')
            else:
                flash('Branch not found!', 'error')
                
    # Get all branches for display
    branches = BranchDivision.query.all()
    return render_template('adminbranchdivision.html', form=form, branches=branches)


@app.route("/admincourse",methods=['GET','POST'])
def admin_course():
    form = AdminCourse()
    if form.validate_on_submit():
        if form.choose.data == '1':  # Add course
            # Create new course
            course_to_create = Courses(courseid=form.courseid.data,
                                     name=form.name.data)
            db.session.add(course_to_create)
            db.session.commit()
            flash('Course added successfully!', 'success')
            
        elif form.choose.data == '2':  # Remove course
            # Find course by course ID
            course = Courses.query.filter_by(courseid=form.courseid.data).first()
            if course:
                db.session.delete(course)
                db.session.commit()
                flash('Course removed successfully!', 'success')
            else:
                flash('Course not found!', 'error')
                
    # Get all courses for display
    courses = Courses.query.all()
    return render_template('adminCourse.html', form=form, courses=courses)


@app.route("/adminclasslocation",methods=['GET','POST'])
def admin_class_location():
    form = AdminClassLocation()
    if form.validate_on_submit():
        if form.choose.data == '1':  # Add location
            # Create new location
            location_to_create = Locations(classLocation=form.classLocation.data,
                                        floor=form.floor.data)
            db.session.add(location_to_create)
            db.session.commit()
            flash('Class location added successfully!', 'success')
            
        elif form.choose.data == '2':  # Remove location
            # Find location by class location
            location = Locations.query.filter_by(classLocation=form.classLocation.data).first()
            if location:
                db.session.delete(location)
                db.session.commit()
                flash('Class location removed successfully!', 'success')
            else:
                flash('Class location not found!', 'error')
                
    # Get all locations for display
    locations = Locations.query.all()
    return render_template('adminClassLocation.html', form=form, locations=locations)




@app.route("/facultydashboard",methods=['GET','POST'])
def faculty_student():
    form = AdminStudent()
    if form.validate_on_submit():
        if form.choose.data == '1':
            pass
        else:
            pass
    return render_template('facultydashboard.html',form=form)


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
        return redirect(url_for('student_dashboard_page',studentid=id))
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
        return redirect(url_for('admin_student'))
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