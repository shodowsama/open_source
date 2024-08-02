import os
import pandas as pd
from openpyxl import load_workbook
from xlrd import open_workbook

# 建立資料夾
if 'data_trainsform' in os.listdir() :
    pass
else :
    os.makedirs('data_trainsform')

# 資料格式整理(刪除空格數較多-最大值減4-的行)
def one_line_clear(data):   
    s1 = data[data.isna().sum(axis=1)<(data.shape[1]-4)].reset_index(drop=True)
    i = 0
    while sum(s1.iloc[i,:] == s1.iloc[i+1,:]) != 0:  
        i += 1
    s2 = s1.drop(index = i)
    s2.columns = s1.iloc[i,:]
    
    return s2 

# 合併儲存格資料(多行欄位名稱合併)
def combin_line_clear(df,sheet):  
    i = 0
    while (df.iloc[i,:].isna().sum()) != (df.iloc[i+1,:].isna().sum()):  
        i += 1
    #找合併儲存格的index
    for item in sheet.merged_cells:
        top_col, top_row, bottom_col, bottom_row = item.bounds
        base_value = item.start_cell.value
        # 調整index
        top_row -= 1
        top_col -= 1
        # 如果設置header，對座標進行調整
        df.iloc[top_row:bottom_row, top_col:bottom_col] = base_value

    cols = []
    for j in range(df.shape[1]):
        col_name = ''
        for s in range(i):
            name = str(df.iloc[s,j]) + '_'
            col_name = col_name + name
        cols.append(col_name)
    df.columns = [col.replace('nan_','').replace('\n','') for col in cols]
    s1 = df.iloc[i:,:]

    s2 = s1.drop(s1.columns[0],axis=1)
    return s2


for file_path , _ , filenames in os.walk(os.path.join('data_source')):
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
# 處理教職員資料
for file_path , _ , filenames in os.walk(os.path.join('data_staff')):
    for filename in filenames :
        f = os.path.join(file_path,filename)
        df = pd.read_excel(f,header=None)
        
        fout = f.replace('data_staff','data_trainsform')
        if 'xlsx' not in fout:    fout = fout.replace('xls','xlsx')
            
        filenam = filename.replace('xlsx','')
        result = one_line_clear(df)
        result.to_excel(fout,sheet_name=filename,index=False)
