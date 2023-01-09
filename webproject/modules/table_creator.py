from webproject import db

def wei_to_eth(wei):
    return wei / 1000000000000000000

def true_false(value):
    return 'True' if value == 1 else 'False'

def yes_no(value):
    return 'Yes' if value == 1 else 'No'

def timestamp_to_date(timeStamp):
    # return timeStamp.strftime('%Y-%m-%d %H:%M')
    return timeStamp[:-10]
    
def asset_type_string(asset_type):
    if asset_type == 1:
        return 'Token'
    if asset_type == 2:
        return 'NFT'
    if asset_type == 3:
        return 'Dapp'
    
def short_hash(hash):
    hash = str(hash)
    return hash[:10] + '...' if len(hash) > 10 else hash

class Field:
    def __init__(self,format,display):
        self.Format = format
        self.Display = display
    def format(self,value):
        if self.Format is None:
            return value
        else:
            return self.Format(value)
        
class TableCreator:
    def __init__(self,table_name,fields,condition=None,actions=["Edit", "Delete","View"]):
        self.table_name = table_name
        self.join_table = None
        self.condition = condition
        self.join_condition = None
        self.actions = actions
        self.fields = {column:field for column,field in fields.items()}

        if 'id' not in self.fields and len(actions) > 0:
            raise Exception('TableCreator: id field is required for actions')
        
    def set_items_per_page(self,items_per_page):
        self.items_per_page = items_per_page
        
    def join(self,table_name,condition):
        self.join_table = table_name
        self.join_condition = condition
        
    def create_view(self):
        fieldlist = ""
        for field in self.fields.keys():
            fieldlist += f"{field},"
        fieldlist = fieldlist[:-1]
        stmt = f"Select {fieldlist} from {self.table_name} "
        if self.join_table:
            stmt += f"join {self.join_table} on {self.join_condition} "
        if self.condition:
            stmt += f"where {self.condition}"
                    
        self.items = list(db.session.execute(stmt))
        
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
        columns = [self.fields[field].Display for field in self.fields if self.fields[field].Display]
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
            for idx,field in enumerate([field_ for field_ in self.fields ]):
                field = self.fields[field]
                if not field.Display:
                    continue
                value = item[idx]
                value = field.format(value)
                html += f'<td>{value}</td>'
            html += '<td><div class="neuro-flex-row">'
            
            self.id = item[0]
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