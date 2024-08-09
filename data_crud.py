import mysql.connector
import pandas as pd
import numpy as np
import os
import copy

staff = 'staff.xlsx'
# 字串元素容許最大字元
num = 300
# 來源資料夾
data_folder = 'data_clean'
# 資料庫名稱
db_name = 'school_db'
# 各表欄位改名前後對照
table_name = 'compare_table'
compare_name = ['tb_Origin','tb_Cover','col_Origin','col_Cover']
compare_element = [80,80,1500,300]
# 校名對照表
data_use = '處理學校.xlsx'
school_compare = 'school_compare'
columns_name = ['origin','cover']
columns_element = [80,80]
# 固定欄位名稱替換
check_cols = ['學校名稱','學年度','學制班別']
change_cols = ['school','year','academic']
# 專任教師數等修改檔名(ex 1-1.專任教師 to 人1-1.專任教師)
filename_change = {'學':'table_learn',
                   '研':'table_study',
                   '校':'table_school',
                   '財':'table_property',
                   '教':'table_teach',
                   '人':'table_employee',}

# 連接資料庫
def db_connet(db_name):
    return mysql.connector.connect(
                host = '127.0.0.1',
                user = 'root',
                password = '00000',
                port = '3306',
                database = db_name        
                )

def sql_grammar(db_conet,grammar):
    db_cursor = db_conet.reconnect()
    db_cursor = db_conet.cursor()
    db_cursor.execute(grammar)
    return db_cursor

class db_crud:
    def __init__(self,db_conet,db_name) -> None:
        self.db_name = db_name
        self.db_conet = db_conet
    # 創建資料庫
    def create_db(self):        
        grammar = 'create database '+ self.db_name
        _ = sql_grammar(self.db_conet,grammar)        
    #　刪除資料庫
    def delet_db(self):
        grammar = 'drop database '+ self.db_name
        _ = sql_grammar(self.db_conet,grammar)
    # 刪除表
    def tb_del(self,table_name):
        grammar = 'set foreign_key_checks = 0; drop table '+ table_name + '; set foreign_key_checks = 1'
        _ = sql_grammar(self.db_conet,grammar)  
    # 刪除資料
    def data_del(self,table_name,col,name_after):
        grammar = 'delete  from ' + table_name +' where ' + col + ' = "' + name_after + '"'
        _ = sql_grammar(self.db_conet,grammar)
    # 叫出資料庫中所有表名
    def db_tables(self):       
        grammar = 'show tables'
        db_cursor = sql_grammar(self.db_conet,grammar)
        tables_name = [table[0] for table in db_cursor.fetchall()]
        return tables_name    
    # 創建對照表
    def compare_tb_create(self,table_name,columns_name,element,pk_number):
        try:
            temp_columns = [columns_name[i] + ' nvarchar(' + str(element[i]) +') ' 
                            for i in range(len(columns_name)) ]
            if pk_number.lower() == 'id':
                grammar = ('create table ' + table_name + '( `id` int not null AUTO_INCREMENT,' +
                            ','.join(temp_columns) + ', PRIMARY KEY (id))')
            else:
                grammar = ('create table ' + table_name + '( ' + ','.join(temp_columns) +
                            ', PRIMARY KEY (' + pk_number.lower() + '))')
            _ = sql_grammar(self.db_conet,grammar)
        except Exception as e: print(e) 
    # 插入對照表
    def compare_tb_insert(self,db,table_name,columns_name,data):
        try:
            grammar = 'set sql_mode="ANSi"'
            _ = sql_grammar(self.db_conet,grammar)
            
            grammar = ('insert into ' + table_name + ' ( ' + 
                        ','.join(columns_name) + ') values (' + 
                        ' %s,'*(len(columns_name)-1) + '%s)' )

            df = data.apply(lambda x: tuple(x),axis=1).values.tolist()
            db_cursor = db.cursor()

            for i in range(len(df)):
                db_cursor.execute(grammar,df[i])
            db.commit()    
        except Exception as e: print(e)
    # 創建表
    def tb_create(self,table_name,columns_name,cols_type,pk_number,compare_table):
        try:
            temp_columns = [columns_name[i] + ' ' + cols_type[i] 
                            for i in range(len(columns_name)) ]
            
            grammar = ('create table ' + table_name + '( `id` int not null AUTO_INCREMENT,' + 
                        ','.join(temp_columns) + ', PRIMARY KEY (id), FOREIGN KEY(school) REFERENCES ' + 
                        compare_table + '(' + pk_number.lower() + ')  ON DELETE CASCADE)')

            _ = sql_grammar(self.db_conet,grammar)
        except Exception as e: print(e)

    # 插入對照表
    def tb_insert(self,db,table_name,columns_name,data):
        try:
            # 刪除過長資料
            grammar = 'set sql_mode="ANSi"'
            _ = sql_grammar(self.db_conet,grammar)

            db_cursor = db.cursor()
            for i in range(len(data)):
                a1 = pd.isna(list(data.iloc[i,:]))
                a2 = pd.Series(data.iloc[i,:].to_dict()).values
                df = tuple([ None  if a1[j] else a2[j]  for j in  range(len(a1)) ])

                grammar = ('insert into ' + table_name + ' ( ' + 
                            ','.join(columns_name) + ') values (' + 
                            ' %s,'*(len(columns_name)-1) + '%s)' ) 

                db_cursor.execute(grammar,df)
            db.commit()   
        except Exception as e: print(e)


try:
    db_crud(db_connet(None),db_name).create_db()    
except mysql.connector.errors.DatabaseError:
    print('資料庫已存在，可用delet_db()刪除後重新設定')
except Exception as e: print(e)

# 資料讀取
def data_to_df(filename):
    f = os.path.join(file_path,filename)
    data = pd.read_excel(f)
    return  data

# 元素資料類型判斷
def simple_digit(x):
    try:
        float(x)
        if str(x).isdigit():
            return 0
        else:
            return 1
    except :
        return -1

# 資料類型轉換
def data_clean(data):
    for column in data.columns :
        if ('代碼' in column)|('名稱' in column):
            continue
        if data[column].dtypes == int :
            data[column] = pd.to_numeric(data[column],downcast='signed',errors='coerce')
            data[column] = data[column].astype('Int64')
        elif data[column].dtypes == float :
            data[column] = pd.to_numeric(data[column],downcast='float',errors='coerce')
        else:
            check = set(data[column])
            check_list = [ simple_digit(x) for x in list(check) ]
            if (check_list.count(-1) <= 2) & ((check_list.count(0) > 0)| (check_list.count(1) > 0)):
                if check_list.count(1) > 0:
                    data[column] = pd.to_numeric(data[column],downcast='float',errors='coerce')
                else:
                    data[column] = np.floor(pd.to_numeric(data[column], errors='coerce')).astype('Int64')
            else:
                continue
    return data

def data_to_detail(filename,filename_change,check_cols,change_cols):
    # 讀取資料
    df = data_to_df(filename)
    data = data_clean(df)
    # 取資料名前編號(ex 學1-1)
    name_before = filename.split('.')[0]
    # 替換後資料名(ex table_learn1at1)
    name_after = [ name_before.replace('-','at').replace(k,v) for k,v in filename_change.items() if k in name_before]
    # 欄位名稱替換前後
    col_before = list(data.columns)
    col_after = []
    col_type = [data[col].dtypes.name  for col in data.columns]
    # 固定欄位名稱替換
    check_copy = copy.deepcopy(check_cols)
    change_copy = copy.deepcopy(change_cols)

    for i in range(len(col_before)):
        set_ck = True
        for ck in check_copy:
            j = check_copy.index(ck)
            if ck in col_before[i]:
                col_after.append(change_copy[j])
                change_copy.remove(change_copy[j])
                check_copy.remove(check_copy[j])
                set_ck = False
        if set_ck:
            col_after.append('col'+str(i)) 
    
    return data, name_before, name_after, col_before, col_after, col_type

for file_path , _ , filenames in os.walk(os.path.join(data_folder)):
    for filename in filenames :
        db = db_connet(db_name)
        db_cursor = db_crud(db,db_name)
        db_tables_in = db_cursor.db_tables()
        if filename.endswith(data_use):
            data = data_to_df(filename).iloc[:,1:]
            # 原始校名重複刪除
            colname = ''.join([col for col in data.columns if '可能校名' in col])
            data = data.drop_duplicates(subset=[colname])
            # 如果學校對照表已經存在，刪除學校對照表
            if school_compare in db_tables_in:
                db_cursor.tb_del(school_compare)                               
            # 建立表
            db_cursor.compare_tb_create(school_compare,columns_name,columns_element,'Origin')
            # 插入數據
            db_cursor.compare_tb_insert(db,school_compare,columns_name,data)
        elif filename.endswith(staff):
            pass
        else:
            data, name_before, name_after, col_before, col_after, col_type = data_to_detail(filename,filename_change,check_cols,change_cols)
            name_after = [ name_before.replace('-','at').replace(k,v)
                           for k,v in filename_change.items() if k in name_before]
            # 如果表名對照表不存在則創建
            if table_name not in db_tables_in:
                db_cursor.compare_tb_create(table_name,compare_name,compare_element,'id')
            # 將表對照資料插入對照表
            df = pd.DataFrame({compare_name[0]:name_before,
                               compare_name[1]:name_after,
                               compare_name[2]:','.join(col_before),
                               compare_name[3]:','.join(col_after)})            
            db_cursor.compare_tb_insert(db,table_name,compare_name,df)

            
            # 如果表存在，刪除表，刪除對照表中該表資料
            if name_after[0] in db_tables_in:
                db_cursor.tb_del(name_after[0])
                db_cursor.data_del(table_name,'tb_Cover',name_after[0])

            archar = 'nvarchar(' + str(num) + ')'
            col_type = [ col.replace('64','').replace('32','').replace('16','').replace('object',archar) for col in col_type]

            db_cursor.tb_create(name_after[0],col_after,col_type,columns_name[0],school_compare)

            db_cursor.tb_insert(db,name_after[0],col_after,data)


