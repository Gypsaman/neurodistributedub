from webproject.models import User
from webproject.modules.ubemail import UBEmail
from webproject import db, create_app
import random
import json


Instructions ='''

A quiz has been created in DNA called "Mid Term".  YOU HAVE ONLY ONE TRY with this one, there is no multiple tries for midterm.

Create a contract named "Midterm" with the following requirements, deploy to sepolia and submit contract address and ABI to DNA.  

YOU HAVE ONLY ONE SUBMISSION on this contract.

Make sure that you use the correct types, visibility and that variable and function names are spelled exactly as they appear here, with the proper case.  
Failure to do so will impact your grade.

Requirements:

1.  Create a structure called "{0}" with the following properties:
    - {1} called "{2}"
    - {3} called "{4}"
    - {5} called "{6}"

2.  Create a variable called "{7}" with the type {0} and public visibility.

3.  Create a variable called "owner" that stores the address of the owner of the contract.

4.  Create a constructor that:
    - Receives 3 parameters of type {1}, {3}, {5}.
    - updates the variable "{7}" with these values.
    - sets the owner of the contract to the sender.

5.  Create a modifier that only permits owner if not returns "You are not the Owner".

6.  Create a function called "{8}" with public visibility that:
    - Receives a parameter of type uint256
    - Updates the {6} property of "{7}".  
    - This function must only be accessed by owner via the modifier.

7.  Create a function called "{9}" with public visibility that:
    - Returns the {0} structure.  
    - It must be accesible to everyone.
        '''
    

exams = {
    1: {"Structure": {"name":"Student","properties":[{"name":"id","type":"uint256"},{"name":"name","type":"string"},{"name":"age","type":"uint256"}]},
        'variable':'student',
        'update_function':'update_age',
        'get_function':'get_student',
        },
    2: {"Structure": {"name":"Car","properties":[{"name":"model","type":"string"},{"name":"year","type":"uint256"},{"name":"miles_per_gallon","type":"uint256"}]},
        'variable':'car',
        'update_function':'update_miles_per_gallon',
        'get_function':'get_car',
        },
    3: {'Structure':{"name":"Exam","properties":[{"name":"name","type":"string"},{"name":"score","type":"uint256"},{"name":"student_id","type":"uint256"}]},
        'variable':'exam',
        'update_function':'update_score',
        'get_function':'get_exam',
        },
    4: {'Structure':{"name":"Book","properties":[{"name":"title","type":"string"},{"name":"author","type":"string"},{"name":"pages","type":"uint256"}]},
        'variable':'book',
        'update_function':'update_pages',
        'get_function':'get_book',
        },
    5: {'Structure':{"name":"Movie","properties":[{"name":"title","type":"string"},{"name":"director","type":"string"},{"name":"year","type":"uint256"}]},
        'variable':'movie',
        'update_function':'update_year',
        'get_function':'get_movie',
        },
    6: {'Structure':{"name":"Product","properties":[{"name":"name","type":"string"},{"name":"price","type":"uint256"},{"name":"quantity","type":"uint256"}]},
        'variable':'product',
        'update_function':'update_quantity',
        'get_function':'get_product',
        },
    7: {'Structure':{"name":"House","properties":[{"name":"street_address","type":"string"},{"name":"city","type":"string"},{"name":"rooms","type":"uint256"}]},
        'variable':'house',
        'update_function':'update_rooms',
        'get_function':'get_house',
        },
    8: {'Structure':{"name":"Animal","properties":[{"name":"name","type":"string"},{"name":"animal_type","type":"string"},{"name":"age","type":"uint256"}]},
        'variable':'animal',
        'update_function':'update_age',
        'get_function':'get_animal',
        },
    9: {'Structure':{"name":"Employee","properties":[{"name":"name","type":"string"},{"name":"position","type":"string"},{"name":"salary","type":"uint256"}]},
        'variable':'employee',
        'update_function':'update_salary',
        'get_function':'get_employee',
        },
    10: {'Structure':{"name":"Country","properties":[{"name":"name","type":"string"},{"name":"population","type":"uint256"},{"name":"area","type":"uint256"}]},
        'variable':'country',
        'update_function':'update_area',
        'get_function':'get_country',
        },
    
}

def get_instructions(exam):
    return Instructions.format(
        exam['Structure']['name'],
        exam['Structure']['properties'][0]['type'],
        exam['Structure']['properties'][0]['name'],
        exam['Structure']['properties'][1]['type'],
        exam['Structure']['properties'][1]['name'],
        exam['Structure']['properties'][2]['type'],
        exam['Structure']['properties'][2]['name'],
        exam['variable'],
        exam['update_function'],
        exam['get_function']
    )

def build_exam_distribution():
    
    exam_distribution = {}
    with create_app().app_context():
        for user in User.query.all():
            exam_distribution[user.student_id] = {"exam_id":random.randint(1,len(exams)),"email":user.email,"name":user.last_name}
    json.dump(exam_distribution,open('./graders/exam_distribution.json','w'))
                
def create_program(exam: int) -> str:
    
    # we use {10} and {11} as place holders for "{" and "}" repectively because the format function confuses it
    
    program = '''
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0;

contract Midterm {10}

    address owner;

    struct {0} {10}
        
        {1} {2};
        {3} {4};
        {5} {6};
    {11}

    {0} public {7};

    modifier onlyOwner {10}
        require(msg.sender==owner,"You are not the Owner");
        _;
    {11}

    constructor({1} {12} _{2}, {3} {13} _{4}, {5} _{6}) {10}
        
        {7}.{2} = _{2};
        {7}.{4} = _{4};
        {7}.{6} = _{6};


        owner = msg.sender;

    {11}
    function {8}(uint256 _{6}) public onlyOwner {10}
        {7}.{6} = _{6};
    {11}

    function {9}() public view returns ({0} memory) {10}
        return {7};
    {11}

{11}
    '''

    return program.format(
        exams[exam]['Structure']['name'],
        exams[exam]['Structure']['properties'][0]['type'],
        exams[exam]['Structure']['properties'][0]['name'],
        exams[exam]['Structure']['properties'][1]['type'],
        exams[exam]['Structure']['properties'][1]['name'],
        exams[exam]['Structure']['properties'][2]['type'],
        exams[exam]['Structure']['properties'][2]['name'],
        exams[exam]['variable'],
        exams[exam]['update_function'],
        exams[exam]['get_function'],
        "{",
        "}",
        "memory" if exams[exam]['Structure']['properties'][0]['type'] == 'string' else "",
        "memory" if exams[exam]['Structure']['properties'][1]['type'] == 'string' else ""
    )
    
def write_all_programs():
    for exam_no in exams.keys():
        program = create_program(exam_no)
        with open(f'./graders/midterm_{exam_no}.sol','w') as f:
            f.write(program)
    
def get_exam(student_id):
    exam_distribution = json.load(open('./graders/exam_distribution.json','r'))
    exam_no = exam_distribution[student_id]
    return exams[exam_no['exam_id']]

def email_exams():
    with create_app().app_context():
        for user in User.query.filter_by(role='student').all():
            exam = get_exam(user.student_id)
            instructions = get_instructions(exam)
            email = UBEmail()
            body = f'{user.first_name},\n\n{instructions}'
            email.send_email(user.email,f'Mid Term Exam',body)
            
if __name__ == '__main__':
    print('MidTermExam.py is meant to be used as module')