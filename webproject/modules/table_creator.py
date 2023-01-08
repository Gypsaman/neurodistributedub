

def wei_to_eth(wei):
    return wei / 1000000000000000000

def timestamp_to_date(timeStamp):
    return timeStamp.strftime('%Y-%m-%d %H:%M')
    
def asset_type_string(asset_type):
    if asset_type == 1:
        return 'Token'
    if asset_type == 2:
        return 'NFT'
    if asset_type == 3:
        return 'Dapp'
    
def short_hash(hash):
    return hash[:10] + '...' if len(hash) > 10 else hash

table_columns = {
    'Transactions': 
        {
            'blockNumber': None, 
            'timeStamp': timestamp_to_date,
            'hash':short_hash, 
            'nonce':None, 
            'blockHash':short_hash,
            'transactionIndex':None, 
            'trans_from':short_hash, 
            'trans_to':short_hash,
            'value':wei_to_eth, 
            'gas':wei_to_eth, 
            'gasPrice':wei_to_eth,
            'isError':None,
            'contractAddress':short_hash
        },
    'Assignments':
        {
            'name': None,
            'due': timestamp_to_date,
            'inputtype': None,
            'grader': None
        },
    'Submissions':
        {
            'assignment':None,
            'submission':None,
            'date_submitted':timestamp_to_date,
            'grade':None
        },
    'Assets':
        {
            'asset_type': asset_type_string,
            'network': None,
            'asset_address': None,
            'time_added': timestamp_to_date,
            'assignment': None
        },
    'Grades':
        {
            'assignment': None,
            'grade': None,
            'dategraded': timestamp_to_date,
        }
    }


def table_creator(table_name, items, items_per_page, page_num, actions=["Edit", "Delete","View"]):
    if len(items) == 0:
        return f'<p>No {table_name} added yet</p>'
    
    pages = len(items) // items_per_page
    if len(items) % items_per_page != 0:
        pages += 1
    start = (page_num -1) * items_per_page
    end = start + items_per_page
    columns = list(table_columns[table_name].keys())
    html = '<table class="neuro-table">'
    html += '<thead>'
    html += '<tr>'    
    for column in columns:
        html += f'<th>{column}</th>'
    if len(actions) > 0:
        html += '<th>Actions</th>'
    html += '</tr></thead>'
    
    
    html += '<tbody>'
    for idx,item in enumerate(items[start:end]):
        html += '<tr>'
        for column in columns:
            value = getattr(item,column)
            if table_columns[table_name][column] != None:
                value = table_columns[table_name][column](value)
            html += f'<td>{value}</td>'
        html += '<td><div class="neuro-flex-row">'
        id = getattr(item,'id')
        if "Edit" in actions:
            html += f'<a href="/{table_name.lower()}/update/{id}"><img src="\static\imgs\pen.svg"></a>'
        if "Delete" in actions:
            html += f'<a href="/{table_name.lower()}/delete/{id}"><img src="\static\imgs\\trash.svg"></a>'
        if "View" in actions:
            html += f'<a href="/{table_name.lower()}/view/{page_num}/{id}"><img src="\static\imgs\\binoculars.svg"></a>'
        html += '</div></td>'
        html += '</tr>'

    next_button = True if pages > page_num else False
    back_button = True if page_num > 1 else False
    
        
    html += '</tbody></table>'
    html += '<div class="neuro-flex-row neuro-table-nav">'
    html += '<div style="height: 30px; width: 30px">'
    if back_button:
        html += f'<a href="/{table_name.lower()}/{page_num - 1}"><img src="/static/imgs/ArrowLeft.svg" style="height: 100%; width: 100%;"></a>'
    html += '</div>'
    html += '<div style="height: 30px; width: 30px">'
    if next_button:
        html += f'<a href="/{table_name.lower()}/{page_num + 1}"><img src="/static/imgs/ArrowRight.svg" style="height: 100%; width: 100%;"></a>'
    html += '</div>'
    html += '</div>'
    
    return html