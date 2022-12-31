from datetime import datetime

def wei_to_eth(wei):
    return wei / 1000000000000000000

def timestamp_to_date(timeStamp):
    return timeStamp.strftime('%Y-%m-%d %H:%M')
    
    
def short_hash(hash):
    return hash[:10] + '...' if len(hash) > 10 else hash

table_columns = {'Transactions': 
    {'blockNumber': None, 
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
     'contractAddress':short_hash}
    }


def table_creator(table_name, items, items_per_page, page_num):
    if len(items) == 0:
        return f'<p>No {table_name} added yet</p>', 0
    
    pages = len(items) // items_per_page
    if len(items) % items_per_page != 0:
        pages += 1
    start = (page_num -1) * items_per_page
    end = start + items_per_page
    columns = list(table_columns[table_name].keys())
    html = '<table class="neuro-table"><thead><tr>'    
    for column in columns:
        html += f'<th>{column}</th>'
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
        html += f'<a href="/{table_name}/update/{{idx}}"><img src="\static\imgs\pen.svg"></a>'
        html += f'<a href="/{table_name}/delete/{{idx}}"><img src="\static\imgs\\trash.svg"></a>'
        html += '</div></td></tr>'

    next_button = True if pages > page_num else False
    back_button = True if page_num > 1 else False
    
        
    html += '</tbody></table>'
    html += '<div class="neuro-flex-row">'
    if back_button:
        html += '<div><button class="btn btn-primary" '
        html += f'onclick="window.location.href='
        html += f"'/transactions/{page_num - 1}'"
        html += '">Back</button></div>'
    if next_button:
        html += '<div><button class="btn btn-primary" '
        html += f'onclick="window.location.href='
        html += f"'/transactions/{page_num + 1}'"
        html += '">Next</button></div>'
    html += '</div>'
    
    return html