import json
import os


def convert():
    with open('./data/roster.csv','r') as f:
        roster = f.readlines()
        
    columns = roster[0][:-1].split(',')
    
    out = {}
    if os.path.exists('./data/roster.json'):
        with open('./data/roster.json','r') as f:
            out = json.load(f)
    
    for line in roster[1:]:
        data = line.split(',')
        student_id = data[0]
        if student_id in out:
            continue
        info = {columns[i]:data[i] for i in range(1,len(columns))}
        info['Course'] = info['Course'][:-1]
        out[student_id] = info
        
    with open('./data/roster.json','w') as f:
        json.dump(out,f)
        
def test_conversion():
    with open('./data/roster.json','r') as f:
        roster = json.load(f)
        
    for student,info in roster.items():
        print(f'{student}: {info["Course"]}')
        
    
if __name__ == '__main__':
    convert()
    test_conversion()
    