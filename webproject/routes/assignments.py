from flask import Blueprint,render_template,request,redirect,url_for,flash
import werkzeug
from flask_login import current_user
from webproject.models import User,Wallet,Assignments,Grades,Submissions
from webproject.modules.table_creator import TableCreator, Field,timestamp_to_date,short_hash,wei_to_eth,asset_type_string
from webproject import db
from datetime import datetime as dt
import os
from os.path import join


from flask_login import login_required

class AttributeDict(dict):
    def __getattr__(self, attr):
        return self[attr]
    def __setattr__(self, attr, value):
        self[attr] = value

UPLOADPATH = os.getenv('UPLOADPATH')
assignments = Blueprint('assignments',__name__)

@assignments.route('/assignments/<int:page_num>')
def assingments(page_num):
    fields = {
            'id': Field(None,None),
            'name': Field(None,'Assignment'),
            'due': Field(timestamp_to_date,'Due Date'),
            'inputtype': Field(None,'Input Type'),
            'grader': Field(None,'Grader'),
    }
    
    table_creator = TableCreator('Assignments',fields,actions=['Edit','Delete'])
    table_creator.set_items_per_page(30)
    table_creator.create_view()
    table = table_creator.create(page_num)

    
    return render_template('assignments/assignments.html',table=table)
@assignments.route('/assignments/edit/<int:id>')
def assignments_edit(id):
    assignment = Assignments.query.filter_by(id=id).first()
    return render_template('assignments/assignments_edit.html',assignment=assignment)

@assignments.route('/addassignment',methods=['GET','POST'])
def add_assignment():
    if request.method == 'POST':
        record = {
            'name':request.form['assignmentName'],
            'due': dt.strptime(request.form['due'],'%Y-%m-%d'),
            'inputtype' : request.form['inputtype'],
            'grader' : request.form['grader'],
        }
        assignment = Assignments.query.filter_by(name=record['name']).first()
        if assignment:
            flash("Assignment already exists")
            return redirect(url_for('assignments.add_assignment'))

        assignment = Assignments(**record)
        db.session.add(assignment)
        db.session.commit()
        return redirect(url_for('assignments.assignments'))
    return render_template('assignments/assignments_add.html')


@assignments.route('/submissionselect')
def submission_select():

    assignments = Assignments.query.all()
    return render_template('assignments/submission_select.html',assignments=assignments)

@assignments.route('/submissionselect',methods=['POST'])
def submission_select_post():
        
    assignment = Assignments.query.filter_by(name=request.form['assignmentName']).first()
    fields = {
            'submission':Field(None,'Submission'),
            'date_submitted':Field(timestamp_to_date,'Date Submitted'),
            'grade': Field(None,'Grade')
    }
    table_creator = TableCreator('Submissions',fields,condition=f"assignment={assignment.id}",actions=[])
    table_creator.set_items_per_page(15)
    table_creator.create_view()
    # table_creator.view(db.session.query(Submissions.assignment,Submissions.submission,Submissions.date_submitted,Submissions.grade).all())
    table = table_creator.create(1)
    
    return render_template('assignments/submission.html',assignment=assignment,table=table)
    
@assignments.route('/submission/<int:submission_id>',methods=['POST'])
def submission_post(submission_id):

    assignment = Assignments.query.filter_by(id=submission_id).first()
    upload_name = ''
    if assignment.inputtype == 'file':
        file_data = request.files['submission']
        file_name = werkzeug.utils.secure_filename(f'{submission_id}_{current_user.id}_{dt.now().strftime("%Y%m%d%H%M%S")}_{file_data.filename}')
        file_data.save(join(UPLOADPATH,file_name))
        upload_name=file_name
    else:
        upload_name = request.form['submission']
        
    record = {
        "user_id":current_user.id,
        "assignment":submission_id,
        "submission":upload_name,
        "date_submitted":dt.now(),
        'grade':None
    }
    submission = Submissions(**record)
    db.session.add(submission)
    db.session.commit()
        
    return render_template('assignments/submissionconfirm.html',assignment=assignment,submission=upload_name)

@assignments.route('/grades/<int:page_num>')
def grades(page_num):
    
    fields = {
        'assignments.name': Field(None,'Assignment'),
        'grade': Field(None,'Grade'),
        'dategraded': Field(timestamp_to_date,'Date Graded'),

    }
    
    table_creator = TableCreator('Grades',fields,actions=[])
    table_creator.join('Assignments','Grades.assignment = Assignments.id')
    table_creator.set_items_per_page(30)
    table_creator.create_view()
    table = table_creator.create(page_num)
    
    return render_template('assignments/grades.html',table=table)
