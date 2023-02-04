import pandas as pd
import json
import requests

def grade_history():
        
    response = requests.get('http://neurodistributed/gradehistory')
    gradehistory = json.loads(response.content)
    df = pd.json_normalize(gradehistory)
    return df.pivot(index=['section','StudentID'], columns='assignment', values='grade')
    
grade_history()