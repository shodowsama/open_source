import os
import pandas as pd
import numpy as np
from openpyxl import load_workbook
from xlrd import open_workbook

# 學期替換
semester_change = {1:'上',2:'下','1':'上','2':'下'}
establish_change = {'國立':'公立'}


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

# 資料表類型轉換
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

for file_path , _ , filenames in os.walk(os.path.join('data_trainsform')):
    # 使用過的資料表
    dat_names = []
    staff_data = pd.DataFrame()

    for filename in filenames :
        f = os.path.join(file_path,filename)
        excel = pd.ExcelFile(load_workbook(f), engine="openpyxl")

        fout = f.replace('data_trainsform','data_clean')
        writer = pd.ExcelWriter(fout)
        # 資料名前輟(學1-2)
        dat_name = filename.split('.')[0]

        # 讀取整理資料
        df = excel.parse(excel.sheet_names[0],header=None)
        data = df.iloc[1:,:].copy()
        columns = df.iloc[0,:]
        # 資料一致性整理
        if any([x == '年度' for x in columns]): columns.replace('年度','學年度',inplace=True)
        data.columns = columns

        if any([x == '設立別' for x in columns]): data['設立別'] = data['設立別'].replace(establish_change)
        if any([x == '學期' for x in columns]): data['學期'] = data['學期'].replace(semester_change)
        if any([x == '日間/進修' for x in columns]): 
            data['學制班別(日間/進修)'] = data['學制班別'] + '(' + data['日間/進修'] + ')'
            del data['學制班別']
            del data['日間/進修']

        print(filename)
        # 教職員資料合併
        if '_staff' in filename:
            # 補足'學年度'欄位
            year = filename.split('_')[0]
            data['學年度'] = int(year)
            # 清除特殊符號
            data = data_clean(data)
            staff_data = pd.concat([staff_data,data],join='outer',axis=0)
        else:
            data = data_clean(data)
        print(data.info())

        data.to_excel(writer,sheet_name = excel.sheet_names[0],index=False)
        writer.close()         

staff_data.to_excel(os.getcwd() + '/data_clean/staff.xlsx',sheet_name='staff',index=False,na_rep = '#N/A')


# 統一欄位名稱[學年度、學期、設立別、學校類別、學校代碼、學校名稱、學制班別]
# 合併分頁後如果有完全相同之兩筆資料則刪除其中一筆
# 如果資料中沒有學年度，將分頁名稱作為替代
# 學期統一替換成'上'、'下'


'''
# 建立資料夾
if 'data_clean' in os.listdir() :
    pass
else :
    os.makedirs('data_clean')


for file_path , _ , filenames in os.walk(os.path.join('data_clean')):
    for filename in filenames :
        f = os.path.join(file_path,filename)
        excel = pd.ExcelFile(load_workbook(f), engine="openpyxl")
        
        fout = f.replace('data_source','data_trainsform')
        writer = pd.ExcelWriter(fout)
        
        #逐excel分頁處理
        for sheet_name in excel.sheet_names:
            df = excel.parse(sheet_name,header=None)
            
            n = 0
            while sum(df.iloc[n,:].isna()) >1 :
                n+=1
                
            if sum(df.iloc[n,:] == df.iloc[n+1,:]) != 0 :
                sheet = excel.book[sheet_name]
                ss = combin_line_clear(df,sheet)
                result = ss[ss.isna().sum(axis=1)<2]

            else :
                result = one_line_clear(df)

            result.to_excel(writer,sheet_name = sheet_name,index=False)
        writer.close()
'''