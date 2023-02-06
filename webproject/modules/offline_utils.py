import pandas as pd
import json
import requests

def grade_history():
        
    response = requests.get('http://neurodistributed.com/gradehistory')
    # response = requests.get('http://127.0.0.1:5000/gradehistory')
    gradehistory = json.loads(response.text)

    df = pd.json_normalize(gradehistory)
    df.to_csv('gradehistory.csv')
    # print(df.pivot(index=['section','StudentID'], columns='assignment', values='grade'))
    
grade_history()