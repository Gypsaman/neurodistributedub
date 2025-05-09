from flask import Blueprint,render_template,request,redirect,url_for,flash
import werkzeug
from flask_login import current_user
from webproject.models import User,Wallet,Assignments,Grades,Submissions, DueDates, Sections
from webproject.modules.table_creator import TableCreator, Field,timestamp_to_date,short_hash,wei_to_eth,asset_type_string, true_false
from graders.github import check_duplicate_repo
from webproject import db
from datetime import datetime as dt
import os
from os.path import join
import json
from webproject.modules.logger import LogType, Log

from flask_login import login_required
from webproject.routes import admin_required


UPLOADPATH = os.getenv('UPLOADPATH')
assignments = Blueprint('assignments',__name__)

@assignments.route('/assignments/<int:page_num>')
@admin_required
def assingments(page_num):
    fields = {
            'id': Field(None,None),
            'name': Field(None,'Assignment'),
            'inputtype': Field(None,'Input Type'),
            'grader': Field(None,'Grader'),
            'Active': Field(true_false,'Active'),
            'grade_category': Field(None,'Grade Category'),
            'retries': Field(None,'Retries')
    }
    
    table_creator = TableCreator('Assignments',fields,actions=['Edit','Delete'])
    table_creator.set_items_per_page(30)
    table_creator.create_view()
    table = table_creator.create(page_num)

    
    return render_template('assignments/assignments.html',table=table)


@assignments.route('/assignments/update/<int:id>')
@admin_required
def assignments_edit(id):
    assignment = Assignments.query.filter_by(id=id).first()
    return render_template('assignments/assignments_edit.html',assignment=assignment)

@assignments.route('/assignments/update/<int:id>',methods=['POST'])
@admin_required
def assigments_edit_post(id):
    assignment = Assignments.query.filter_by(id=id).first()
    assignment.name = request.form['assignmentName'].strip()
    assignment.inputtype = request.form['inputtype']
    assignment.grader = request.form['grader']
    assignment.active = True if 'active' in request.form else False
    assignment.retries = request.form['retries']
    assignment.grade_category = request.form['grade_category']
    
    db.session.commit()
    
    return redirect(url_for('assignments.assingments',page_num=1))

@assignments.route('/addassignment',methods=['GET','POST'])
@admin_required
def add_assignment():
    if request.method == 'POST':
        
        record = {
            'name':request.form['assignmentName'].strip(),
            'inputtype' : request.form['inputtype'],
            'grader' : request.form['grader'].strip(),
            'active' : True if 'active' in request.form else False,
            'grade_category': request.form['grade_category'].strip(),
            'retries': request.form['retries']
        }
        assignment = Assignments.query.filter_by(name=record['name']).first()
        if assignment:
            flash("Assignment already exists")
            return redirect(url_for('assignments.add_assignment'))

        assignment = Assignments(**record)
        db.session.add(assignment)
        db.session.commit()
        return redirect(url_for('assignments.assingments',page_num=1))
    return render_template('assignments/assignments_add.html')

@assignments.route('/assignments/delete/<int:id>')
@admin_required
def del_assigment(id):
    assgnm = Assignments.query.filter_by(id=id).first()
    if assgnm:
        db.session.delete(assgnm)
        db.session.commit()
    return redirect(url_for('assignments.assingments',page_num=1))


@assignments.route('/submissionselect')
@login_required
def submission_select():

    assignments = Assignments.query.filter(Assignments.active==True,Assignments.inputtype != "none").all()
    
    return render_template('assignments/submission_select.html',assignments=assignments)

@assignments.route('/submissionselect',methods=['POST'])
@login_required
def submission_select_post():
        
    assignment = Assignments.query.filter_by(name=request.form['assignmentName']).first()
    submissions = Submissions.query.filter_by(user_id=current_user.id,assignment=assignment.id).count()
    max_submission = (submissions >= assignment.retries) if submissions else False
    duedate = DueDates.query.filter_by(assignment=assignment.id,section=current_user.section).first()
    fields = {
            'id': Field(None,None),
            'submission':Field(None,'Submission'),
            'date_submitted':Field(timestamp_to_date,'Date Submitted'),
            'grade': Field(None,'Grade')
    }
    actions =  []
    table_creator = TableCreator('Submissions',fields,
                                 condition=f"assignment={assignment.id} and user_id={current_user.id}",
                                 actions=actions)
    table_creator.set_items_per_page(15)
    table_creator.create_view()
    table = table_creator.create(1)
    Log(LogType.ASSIGNMENT,current_user.id,f'{assignment.name}')
    
    return render_template('assignments/submission.html',assignment=assignment,table=table,duedate=duedate,max_submission=max_submission)
    
@assignments.route('/submission/<int:submission_id>',methods=['POST'])
@login_required
def submission_post(submission_id):

    assignment = Assignments.query.filter_by(id=submission_id).first()
    submission = ''

    if assignment.inputtype == 'file':
        file_data = request.files['submission']
        file_name = werkzeug.utils.secure_filename(f'{submission_id}_{current_user.id}_{dt.now().strftime("%Y%m%d%H%M%S")}_{file_data.filename}')
        file_data.save(join(UPLOADPATH,file_name))
        submission=file_name

    elif assignment.inputtype == 'address_abi':
        contract = request.form['submission']
        abi = request.form['abi']
        network = request.form['network']
        wallet_record = Wallet.query.filter_by(user_id=current_user.id).first()
        if wallet_record is None:
            flash('You do not have a wallet setup, Cannot submit')
            return redirect(url_for('assignments.submission_select'))
        wallet = wallet_record.wallet
        if wallet == contract:
            flash('You cannot submit your wallet address. You need to submit the contract address')
            return redirect(url_for('assignments.submission_select'))
            
        submission = json.dumps({
            'contract':contract,
            'abi':abi,
            'wallet':wallet,
            'network':network,
            'user_id':{"system_id":current_user.id,"student_id":current_user.student_id}
        })

    elif assignment.inputtype == 'Github Repository':
        submission = request.form['submission']
        if not submission.startswith('https://github.com'):
            flash('You need to submit a Github Repository: https://github.com/username/repo')
            return redirect(url_for('assignments.submission_select'))
        if check_duplicate_repo(submission_id,submission,current_user.id):
            flash('You have are submitting a repository used by another student')
            return redirect(url_for('assignments.submission_select'))
        
    else:
        submission = request.form['submission']

    record = {
        "user_id":current_user.id,
        "assignment":submission_id,
        "submission":submission,
        "date_submitted":dt.now(),
        'grade':None
    }
    submission_record = Submissions(**record)
    db.session.add(submission_record)
    db.session.commit()
        
    return render_template('assignments/submissionconfirm.html',assignment=assignment,submission=submission)

@assignments.route('/grades/<int:page_num>')
@login_required
def grades(page_num):
    
    fields = {
        'grades.id': Field(None,None),
        'assignments.name': Field(None,'Assignment'),
        'grade': Field(None,'Grade'),
        'dategraded': Field(timestamp_to_date,'Date Graded'),

    }
    actions =  []
    table_creator = TableCreator('Grades',fields,condition=f'user_id={current_user.id}',actions=actions)
    table_creator.join('Assignments','Grades.assignment = Assignments.id')
    table_creator.set_items_per_page(30)
    table_creator.create_view()
    table = table_creator.create(page_num)
    
    return render_template('assignments/grades.html',table=table)

@assignments.route('/gradehistory')
def grade_history():
	
    qry = '''
	SELECT student_id, sections.section, assignment, assignment_id, grade 
 	FROM User
  	join Sections on User.section = Sections.id  
    join 
    (SELECT user_id, assignments.id as assignment_id, assignments.name as assignment, grade from Grades join Assignments on Grades.assignment = Assignments.id) as g
    on User.id = g.user_id
    where User.role = 'student' 
 	'''
  
    history = db.engine.execute(qry)
    return [{'StudentID':row.student_id,'section':row.section,'assignment':f'{row.assignment_id:02d}-{row.assignment}','grade':row.grade} for row in history]


@assignments.route("/assignments_due/<int:assignment>")
@admin_required
def assigments_due(assignment):
    
    fields = {
        "due_dates.id": Field(None, None),
        "assignments.name": Field(None, "Assignment"),
        "section": Field(None, "Section"),
        "duedate": Field(timestamp_to_date, "Due Date"),
    }
    actions = ["Edit", "Delete"]
    table_creator = TableCreator("Due_Dates", fields, condition=f"due_dates.assignment={assignment}",actions=actions)
    table_creator.set_items_per_page(15)
    table_creator.join("Assignments", "assignments.id=due_dates.assignment")
    table_creator.create_view()
    table = table_creator.create(1)
    return render_template("assignments/assignmentsdue.html", table=table,assignment=assignment)

@assignments.route('/add_assgn_duedate/<int:id>')
@admin_required
def add_duedate(id):
    assignments = Assignments.query.all()
    sections = Sections.query.all()
    return render_template('assignments/add_assgn_duedate.html', assignments=assignments,selected=id,sections=sections)

@assignments.route('/add_assgn_duedate', methods=['POST'])
@admin_required
def add_duedate_post():
    record = {
        'assignment': request.form['assignment'],
        'section': request.form['sectionid'],
        'duedate': dt.strptime(request.form['duedate'].replace('T',' '),'%Y-%m-%d %H:%M')
    }
    duedate = DueDates(**record)
    db.session.add(duedate)
    db.session.commit()
    return redirect(url_for('assignments.assigments_due',assignment=record["assignment"]))


@assignments.route('/due_dates/update/<int:id>')
@admin_required
def edit_duedate(id):
    duedate = DueDates.query.filter_by(id=id).first()
    assignment = Assignments.query.filter_by(id=duedate.assignment).first().name
    section = Sections.query.filter_by(id=duedate.section).first().section
    return render_template('assignments/edit_duedate.html',duedate=duedate,assignment_name=assignment,section_name=section)

@assignments.route('/due_dates/update',methods=['POST'])
@admin_required
def edit_duedate_post():

    assignment = Assignments.query.filter_by(name=request.form['assignment']).first().id
    section = Sections.query.filter_by(section=request.form['sectionid']).first().id
    duedate = DueDates.query.filter_by(assignment=assignment,section=section).first()
    duedate.assignment = assignment
    duedate.section = section
    duedate.duedate = dt.strptime(request.form['duedate'].replace('T',' '),'%Y-%m-%d %H:%M')
    
    db.session.commit()
    return redirect(url_for(f'assignments.assigments_due',assignment=assignment))
    
@assignments.route('/due_dates/delete/<int:id>')
@admin_required
def del_duedate(id):
    duedate = DueDates.query.filter_by(id=id).first()
    assignment = duedate.assignment
    db.session.delete(duedate)
    db.session.commit()
    return redirect(url_for(f'assignments.assigments_due',assignment=assignment))

