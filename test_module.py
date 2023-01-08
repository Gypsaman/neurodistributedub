from webproject import create_app, db
from webproject.models import Assignments,Submissions,Grades, User
from webproject.modules.table_creator import TableCreator, Field,timestamp_to_date,short_hash,wei_to_eth,asset_type_string


with create_app().app_context():
    
    fields = {
        'id' : Field(None,0),
        'Assignment': Field(None,1),
        'Grade': Field(None,2),
        'Date Graded': Field(timestamp_to_date,3)

    }
    
    
    table_creator = TableCreator('Grades',fields,actions=[])
    table_creator.set_items_per_page(30)
    table_creator.view(db.session.query(Grades.id,Assignments.name,Grades.grade,Grades.dategraded).join(Assignments).all())
    table = table_creator.create(1)
    print(table)
