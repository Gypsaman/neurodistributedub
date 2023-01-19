import json


def convert():
    with open('./data/roster.csv','r') as f:
        roster = f.readlines()
        
    columns = roster[0][:-1].split(',')
    out = {}
    for line in roster[1:]:
        data = line.split(',')
        info = {columns[i]:data[i] for i in range(1,len(columns))}
        info['Course'] = info['Course'][:-1]
        out[data[0]] = info
        
    with open('./data/roster.json','w') as f:
        json.dump(out,f)
        
def test_conversion():
    with open('./data/roster.json','r') as f:
        roster = json.load(f)
        
    for student,info in roster.items():
        print(f'{student}: {info["Course"]}')
        
convert()
test_conversion()
    