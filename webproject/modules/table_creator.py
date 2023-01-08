

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

class Field:
    def __init__(self,format,offset):
        self.Format = format
        self.Offset = offset
    def format(self,value):
        if self.Format is None:
            return value
        else:
            return self.Format(value)
        
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
    # 'Assignments':
    #     {
    #         'name': None,
    #         'due': timestamp_to_date,
    #         'inputtype': None,
    #         'grader': None
    #     },
    # 'Submissions':
    #     {
    #         'assignment':None,
    #         'submission':None,
    #         'date_submitted':timestamp_to_date,
    #         'grade':None
    #     },
    # 'Assets':
    #     {
    #         'asset_type': asset_type_string,
    #         'network': None,
    #         'asset_address': None,
    #         'time_added': timestamp_to_date,
    #         'assignment': None
    #     },
    # 'Grades':
    #     {
    #         'id' : Field(None,0),
    #         'Assignment': Field(None,1),
    #         'Grade': Field(None,2),
    #         'Date Graded': Field(timestamp_to_date,3)
    #         # {'Format': timestamp_to_date, 'Offset':3}
    #     }
    }

class TableCreator:
    def __init__(self,table_name,fields,actions=["Edit", "Delete","View"]):
        self.table_name = table_name
        self.actions = actions
        self.fields = {column:field for column,field in fields.items() if column != 'id'}
        self.id = fields['id'] if 'id' in fields else None
        if self.id is None and len(actions) > 0:
            raise Exception('TableCreator: id field is required for actions')
        
    def set_items_per_page(self,items_per_page):
        self.items_per_page = items_per_page
        
    def view(self,view):
        self.items = view
          
        
    def create(self,page_num):
        if len(self.items) == 0:
            return f'<p>No {self.table_name} added yet</p>'
        
        pages = len(self.items) // self.items_per_page
        if len(self.items) % self.items_per_page != 0:
            pages += 1
        start = (page_num -1) * self.items_per_page
        end = start + self.items_per_page
        columns = [field for field in self.fields.keys() if field != 'id']
        html = '<table class="neuro-table">'
        html += '<thead>'
        html += '<tr>'    
        for column in columns:
            html += f'<th>{column}</th>'
        if len(self.actions) > 0:
            html += '<th>Actions</th>'
        html += '</tr></thead>'
        
        
        html += '<tbody>'
        for item in self.items[start:end]:
            html += '<tr>'
            for column in columns:
                field = self.fields[column]
                value = item[field.Offset]
                value = field.format(value)
                html += f'<td>{value}</td>'
            html += '<td><div class="neuro-flex-row">'
            
            if "Edit" in self.actions:
                html += f'<a href="/{self.table_name.lower()}/update/{self.id}"><img src="\static\imgs\pen.svg"></a>'
            if "Delete" in self.actions:
                html += f'<a href="/{self.table_name.lower()}/delete/{self.id}"><img src="\static\imgs\\trash.svg"></a>'
            if "View" in self.actions:
                html += f'<a href="/{self.table_name.lower()}/view/{page_num}/{self.id}"><img src="\static\imgs\\binoculars.svg"></a>'
            html += '</div></td>'
            html += '</tr>'

        next_button = True if pages > page_num else False
        back_button = True if page_num > 1 else False
        
            
        html += '</tbody></table>'
        html += '<div class="neuro-flex-row neuro-table-nav">'
        html += '<div style="height: 30px; width: 30px">'
        if back_button:
            html += f'<a href="/{self.table_name.lower()}/{page_num - 1}"><img src="/static/imgs/ArrowLeft.svg" style="height: 100%; width: 100%;"></a>'
        html += '</div>'
        html += '<div style="height: 30px; width: 30px">'
        if next_button:
            html += f'<a href="/{self.table_name.lower()}/{page_num + 1}"><img src="/static/imgs/ArrowRight.svg" style="height: 100%; width: 100%;"></a>'
        html += '</div>'
        html += '</div>'
        
        return html