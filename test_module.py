from graders.check_submissions import check_submissions
from webproject.modules.table_creator import TableCreator,Field, only_contract, timestamp_to_date
from webproject import db, create_app

# check_submissions()

def test_table():

    submission_fields = {
        "assignments.name": Field(None, "Assignment"),
        "submission": Field(only_contract, "Submission"),
        "date_submitted": Field(timestamp_to_date, "Submitted"),
        "grade": Field(None, "Grade")
    }
    actions=[]
    table_creator = TableCreator("Submissions", submission_fields, condition=f"user_id = {19}", actions=actions)
    table_creator.join("Assignments", "Submissions.assignment == Assignments.id")
    table_creator.set_items_per_page(35)
    table_creator.create_view()
    submissions_table = table_creator.create(1)

with create_app().app_context():    
    test_table()