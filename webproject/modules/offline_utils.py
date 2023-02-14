import pandas as pd
import json
import requests
from webproject.modules.ubemail import UBEmail
from webproject.modules import roster

def grade_history():
        
    response = requests.get('http://neurodistributed.com/gradehistory')
    # response = requests.get('http://127.0.0.1:5000/gradehistory')
    gradehistory = json.loads(response.text)
    

    df = pd.json_normalize(gradehistory)
    df.to_csv('gradehistory.csv')
    
    pt = df.pivot_table(index=['section','StudentID'], columns='assignment', values='grade', aggfunc='sum')
            
    return pt
    
def Assignments_not_completed():
    
    students = roster.open_roster_encrypted()
    
    grades = grade_history()
    
    columns = grades.columns.tolist()
    for idx,row in grades.iterrows():
        
        body = ''
        for col in columns:
            if pd.isna(row[col]) or row[col] == 0:
                body += f'\t{col}\n'
        if body == '':
            continue
            
        student_id = idx[1]
        
        body = f"{students[student_id]['Student Name']},\n\nYou have not completed the following assignments:\n" + body
        
        if 'Wallet' in body:
            body += f"\n***** YOUR WALLET IS NECESSARY FOR MIDTERMS "
            body += f"\n***** YOUR WILL NOT BE ABLE TO SUBMIT WITHOUT THE WALLET\n"
        
        email = UBEmail()
        email.send_email(students[student_id]['Preferred Email'],'Assignments not completed',body)
        
if __name__ == '__main__':
    grade_history()