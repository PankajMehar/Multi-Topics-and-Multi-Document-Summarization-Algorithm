# MEMDS
#### 2017/01/17
* 將各檔案做第一階段資料處理，接下來要做分隔時間的判定
---------------------------------------
#### 2017/01/12
* 轉換平台至windows, 避免處理文字編碼錯誤，接加上with open (docfile,'r', encoding = 'utf8')
---------------------------------------
#### 2017/01/10
* 重新調整程式架構,將流程都整理到main.py檔案之中
  1. 透過url的檔案，將新聞資料從網站上抓下來
  2. 將抓下來的資料進行文字轉換與處理，存到strmming_data中
  - [ ] 要建立一個機制可以輸入分隔的時間，自動將文字作時間分割處理
  - [ ] 要將分析的設置變數拉出來

#### 2017/01/09
* 將各主題的時間開頭時間對齊做分析，門檻0.5, 結果在20180109_result.txt中
- [ ] 將單純的歐式距離分析製作出來
- [ ] 需要設計門檻值，在將數據跑出來
---------------------------------------
#### 2017/01/08~09
* 檢查抓取得資料是否有問題
- [X] CNN - brexit
- [X] CNN - catalan
- [X] CNN - crimea
- [X] CNN - gravitational
- [X] CNN - hk
- [X] CNN - missile
- [X] CNN - sewol
- [X] CNN - syria
- [X] CNN - turkish

- [X] NewYorkTimes - brexit
- [X] NewYorkTimes - catalan
- [X] NewYorkTimes - crimea
- [X] NewYorkTimes - gravitational
- [X] NewYorkTimes - hk
- [X] NewYorkTimes - missile
- [X] NewYorkTimes - sewol
- [X] NewYorkTimes - syria
- [X] NewYorkTimes - turkish

- [X] Theguardian - brexit
- [X] Theguardian - catalan
- [X] Theguardian - crimea
- [X] Theguardian - gravitational
- [X] Theguardian - hk
- [X] Theguardian - missile
- [X] Theguardian - sewol
- [X] Theguardian - syria
- [X] Theguardian - turkish
---------------------------------------
#### 2017/01/07
* 將6個主題資料擷取完畢
- [X] 將所有的資料進行相似度分析
---------------------------------------
#### 2017/01/06
* 加入6個主題資料
---------------------------------------
#### 2017/12/24
* 補上accuracy的資料
* 預期新增的主題:
  1. [嘉爾泰隆獨立事件 - catalan independence site: cnn.com daterange:2017-09-01..2017-12-31](https://en.wikipedia.org/wiki/Catalan_independence_movement)
  2. (iphone X 09/01~12/01)
  3. [北韓飛彈試射 - North Korean missile site: cnn.com daterange:2017-08-01..2017-09-30](https://en.wikipedia.org/wiki/2017_North_Korean_missile_tests#Mid-range_launch_over_Japan)
  4. [敘利亞化學攻擊 - Syria chemical attack site:cnn.com (04/01/2017~06/01/2017)](https://en.wikipedia.org/wiki/Khan_Shaykhun_chemical_attack)
  5. [土耳其政變 - Turkish coup attempt site:theguardian.com (07/01/2016~08/01/2016)](https://zh.wikipedia.org/wiki/2016%E5%B9%B4%E5%9C%9F%E8%80%B3%E5%85%B6%E6%94%BF%E8%AE%8A)
  6. [英國脫歐 - Brexit vote site: cnn.com (06/01/2016~07/31/2016)](https://zh.wikipedia.org/wiki/%E8%8B%B1%E5%9C%8B%E5%8E%BB%E7%95%99%E6%AD%90%E7%9B%9F%E5%85%AC%E6%8A%95#%E6%8A%95%E7%A5%A8%E7%B5%90%E6%9E%9C)
  7. [重力波 - gravitational wave site:cnn.com (01/01/2016~04/01/2016)](https://zh.wikipedia.org/wiki/GW150914)
---------------------------------------
#### 2017/12/18
* 修改parsing的方式，避免沒有紀錄的資料被處理
* 結果記錄在20171218_result.txt

---------------------------------------
#### 2017/12/17
* 增加analysis_auto.py可以自動抓取某一資料夾內的資料，依據日子來做分析計算出相似度
* 將分析資料的excel計算出ACC, P, R, F1
* 修改一些檔案名稱
* 已經將正確率等做出來！！！！ 但是需要再看一下怎麼處理資料最好
reference: http://d0evi1.com/sklearn/model_evaluation/
---------------------------------------
#### 2017/12/14
* 將第一天的資料以TF-PDF做分析,取得結果沒有特別明顯
* TF-IDF計算出來的結果放在分析資料.XLSX 只有4/16的錯誤率
---------------------------------------
#### 2017/12/13
* 將第一天的資料作分析，tf-idf cosines有不錯的結果(應該)
---------------------------------------
#### 2017/12/12
* 將CNN / 衛報的資料處理完成
* 將第一天的資料找出來準備進行分析
---------------------------------------
#### 2017/12/11
* 將hk的資料抓取完畢
* 將世越號資料抓取完畢
- [x] 開始進行分類比對
---------------------------------------
#### 2017/12/10
* 設計抓新聞的機制(衛報)
* 將crimea的資料抓完
* 將資料夾名稱重新設計
- [x] 將其他的兩個主題抓完
---------------------------------------
#### 2017/12/06
* 完成餘弦相似度，且確認可以直接套用idf-cosine與pdf-cosine
- [x] 接著做 precision, recall, F1的計算
(http://blog.csdn.net/quiet_girl/article/details/70830796)
---------------------------------------
#### 2017/12/01
* 完成tf-pdf驗證與計算
* 接著做pdf-cosine
---------------------------------------
#### 2017/11/27
* 完成tf-idf驗證
* 了解其他tf-idf的計算方式
* 預計接著實做pdf
---------------------------------------
#### 2017/11/25
* 完成text_to_vector
* 完成tf
- [x] 預計下次完成idf計算   log(出現的文件次數/總文件數)
---------------------------------------
#### 2017/11/22
* 找出目前可直接套用tfidf的package
* 自建tfidf的function
---------------------------------------
#### 2017/11/20
* 將原本的code重構
* 將蒐集到的新聞報導，根據不同的主題先找出各新聞的時間點
- [x] 將各文件的Sentence Group矩陣轉換出來單一文件