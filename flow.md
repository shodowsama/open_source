# 資料清理與轉換

## 資料清理

### 前處理

* 將**1-1.專任教師**、**2.外籍專任教師**等手動改名為**人1-1.專任教師**、**人2.外籍專任教師**，目的是在輸入SQL資料庫中保持一致性，並有利於資料提取
* 設置git
  ```
  git init  
  git add .  
  git commit -m ' `<此階段任務名稱>` '  
  git remote add `<自訂名稱>` `<git 網址https> `  
  git push -u `<自訂名稱>` master  
  ```
* [虛擬環境建置](https://medium.com/lifes-a-struggle/python-%E8%99%9B%E6%93%AC%E7%92%B0%E5%A2%83%E7%9A%84%E5%BB%BA%E7%AB%8B-%E4%BB%A5-vscode-%E4%BD%BF%E7%94%A8%E6%83%85%E5%A2%83%E7%82%BA%E4%BE%8B-3a88b87d039d)

### 資料前處理

1. 運行**data_cover.py**，用於將合併儲存格是的欄位統一，並刪去多餘的欄位或資料(ex:統計說明)。原始資料放置於 **data_source**，教職員資料放於**data_staff**，修改後資料放置於 **data_trainsform。**
2. 運行**data_clean.py**，用於將教職員資料合併，檔名為**staff**，修改後資料放置於 **data_clean**，具體整理如下:
   1. **staff** 資料增加學年度
   2. **學期**統一替換為**上、下**
   3. **設立別**中**國立**統一替換為**公立**
   4. 學校名稱，學年度，學期：欄位統一化
   5. 若有**日間/進修**欄位則與**學制班別**進行合併
   6. 不可辨識符號如 : '-'、'...' 等替換為NA
   7. 僅讀取**第一個**分頁
3. 運行**data_crud.py**，將**data_clean**匯入mysql中，表名如learn2_2替換為learn2at2。
   SQL(1452 error)：有學校名稱不在**處理學校.xlsx**中，
   SQL(1406 error)：資料內容過長
4.
