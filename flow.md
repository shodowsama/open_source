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
2. 運行**data_clean.py**，用於將資料中分頁合併，將完全相同的兩筆資料刪除，將遺失值填補為na，修改後資料放置於 **data_clean**。
3. 將新年度處理學校資料放入**data_trainsform**資料夾中。
4. 資料檢查，統合教職員資料，對NA資料進行處理。
