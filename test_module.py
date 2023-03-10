from graders.check_submissions import check_submissions
from webproject import create_app, db
from webproject.models import Submissions
# with create_app().app_context():
#     sub = Submissions.query.filter_by(user_id=1,assignment=12).first()
#     sub.grade = None
#     db.session.commit()

import re
# contract_location = re.findall('[\\\\]',"once a upon a time with open('.\\contracts\\newContract.sol','r')")

contract_location = re.findall('[\\\\/.a-zA-Z0-9_]*.sol',"once a upon a time with open('./contracts/newContract.sol','r')")
for i in contract_location:
    print(i)
        
# check_submissions()
