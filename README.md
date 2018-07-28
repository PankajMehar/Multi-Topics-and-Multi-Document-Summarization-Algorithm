# MEMDS

#### 2018/07/28
資料流程：
1. 執行main.py ->讀取指定的新聞資料夾產生各天的資料，如arrange_day_100\day0_CNN_gravitational_1.txt
2. 執行analysis_auto.py -> 產生arrange_day_0\analysis_temp.json與analysis.csv
    - analysis.csv是做各種不同相似度門檻的資料，就是在做分析每日新聞群體的工作
3. 執行daily_data_clusting.py ->產生arrange_day_0\first_clusting_result.json
4. 執行daily_group_relation.py ->產生arrange_day_0\clusting_tree_value.json
    - 分群各新聞事件
5. 執行clusting_tree_analysis.py ->產生final_group_file\{門檻值}.json 跟jsonfinal_group_file_reference\{門檻值}.json
6. 執行analysis_clusting.py ->產生arrange_day_0\res_cos.csv等
7. 執行semantic_analysis.py ->產生分析資料
    - step1() # 產生各群組的資料，並在最後產生出group_number.json的資料
    - step2() # 根據各群組的資料進行相似度比較, 最後產生group_' + str(group_day) + '_%s.json檔案
    - step3() # 將group_data_%s/%s內的json檔案讀出來，並轉換成pajek 的.net檔案
    - step4() # 進行main path分析後產生group_data_%s/%s/main_path.json
    - step5() # 根據主路境內的檔案產生摘要
    - 產生的摘要資料會分別存在textrank / lexrank / main_path_summary(本研究的摘要集) /text_rank_simple, 整理好的資料放置在https://drive.google.com/open?id=1eg7daI1lB9MPCtMUQK_ikiEccMyHMh26
8. 計算Rouge值
    - 下載 https://github.com/RxNLP/ROUGE-2.0 套件
    - 將資料集內的reference檔案(參考摘要)放到projects/test-summarization/reference
    - 將資料及內的system檔案(系統摘要)放到projects/test-summarization/system
    - 執行java -jar rouge2-xx.java 會將計算出來的資料產生在results.csv
    - 跑出來的檔案已經手動整理到Rouge_Final檔案中
    - 最後論文內容根據裡面的資料撰寫結果

---------------------------------------
#### 2017/03/24 
* main_path的文本計算完成 -> semantic_analysis.py
* textrank的文本計算完成 -> mainpath_textrank_summary.py
* lexrank的文本計算完成 - > lexrank_summary.py
* 以0.17為標準穩各文件的比對應該為
  -  group 0 is: {'brexit'} 
  -  group 1 is: {'missile'} 
  -  group 2 is: {'brexit'} 
  -  group 3 is: {'brexit'} 
  -  group 4 is: {'brexit'} 
  -  group 5 is: {'brexit'} 
  -  group 6 is: {'catalan'} 
  -  group 7 is: {'catalan'} 
  -  group 8 is: {'crimea'} 
  -  group 9 is: {'crimea'} 
  -  group 10 is: {'gravitational'} 
  -  group 11 is: {'gravitational'} 
  -  group 12 is: {'brexit'} 
  -  group 13 is: {'hk'} 
  -  group 14 is: {'catalan'} 
  -  group 15 is: {'sewol'} 
  -  group 16 is: {'syria'} 
  -  group 17 is: {'syria'} 
  -  group 18 is: {'turkish'} 
---------------------------------------
#### 2017/03/22
* 所有的主路徑都算出來了
---------------------------------------
#### 2017/03/17
* 建立analysis_clusting.py 去分析final_group_file中的資料
* 最後算出來精準度最高的關係度為0.17, 資料在arrange_day_0\res.csv
---------------------------------------
#### 2017/03/15
* 將各關係度的資料都跑出來，下一步要測試哪一個參數出來的分群正確率最高
- [X] 需要了解當預測資料大於原始資料時的recall rate最好的算法
---------------------------------------
#### 2017/03/08
* 增加Pajek.py檔案做pajek的處理與分析
* [Pajek操作](https://howtorapeurjob.tumblr.com/post/171626802116)
---------------------------------------
#### 2017/03/05
* 將資料做完門檻分析
* 將資料繪圖
* 將資料儲存成pejak可以操作的結構
* 透過pajek找出主路徑，並存圖為pajek_mainpath.jpg
![image](https://github.com/moveurbody/MEMDS/blob/master/pajek_main_path.png)
---------------------------------------
#### 2017/03/04
* 將第22群的資料擷取出來，轉變成json檔案，並完成sentence group的定義
* 存檔名稱為group_22.json
---------------------------------------
#### 2017/02/28
* 分群的個檔案找出來跟顯示完成
---------------------------------------
#### 2017/02/23
* 將樹狀圖做圖形的調整跟相關聯的群組判斷做出來
---------------------------------------
#### 2017/02/21
* 利用clusting_tree_analysis輸入自訂的門檻值，顯示出完整的樹狀圖
---------------------------------------
#### 2017/02/07
* 每天的運算分析數據完成，透過daily_group_relation.py產生clusting_tree_values.json
- [ ] 找出可以做完整路徑的演算法
---------------------------------------
#### 2017/02/04
* 調整存入資料格式
- [ ] 將檔案根據每天與後面的檔案進行關聯分析

        {
          "max_day": 113,
          "daily_data": [
            {
              "day": 0,
              "file_info":[]
              "compare_day": [
                {
                  "day": 1,
                  "file_info":[]
                  "process_group": [[]],
                  "cos": [],
                  "tf_idf": [],
                  "tf_pdf": []
                },
                {
                  "day": 2,
                  "process_group": [[]],
                  "cos": [],
                  "tf_idf": [],
                  "tf_pdf": []
                }
              ]
            }
          ]
        }
---------------------------------------
#### 2017/02/02
* 將資料存入檔案中以利後面的分群
---------------------------------------
#### 2017/02/01
* 找出每個分群中代表性的資料

        每個群中的關係都有個關係係數
        比如A,B的係數為0.3 B,C係數為0.6 C,D係數為0.4 AC係數為0.7

        最具代表性的應該是由ABC三個來比較，因為他們的關係次數最多，但誰最具代表？

        A=0.3*0.7
        B=0.3*0.6
        C=0.7*0.6
        所以C>B>A

        如果只有兩個那誰為代表都一樣
        如果兩個，包含兩個以上算出來的係數一樣，選誰都一樣
---------------------------------------
#### 2017/01/31
* 將各點之間的關係匯出
* 尋找最好的分群方法
* 將各關係的分群方法做出(直接把有關連的列為同一群)
---------------------------------------
#### 2017/01/22
- [X] 找出對齊時間的資料
- [X] 找出均分15天的資料
- [X] 找出均分16天的資料
- [X] 找出均分31天的資料
- [X] 找出均分39天的資料
- [X] 找出均分46天的資料
- [X] 找出均分55天的資料
- [X] 找出均分59天的資料
- [X] 找出均分100天的資料
- [X] 找出均分113天的資料
---------------------------------------
#### 2017/01/21
- [X] 將每天跑出來的相似度資料抽離，並存成一個json檔案
- [X] 將單純的歐式距離分析製作出來
- [X] 需要設計門檻值，再將數據跑出來
- [X] 讀入json檔案，再根據門檻值將資料輸出
---------------------------------------
#### 2017/01/18
* 將預計重新計算時間的邏輯完成，會產生一個json檔案，後續用這個檔案去產生需要分析的資料
* 產生分析資料已完成
---------------------------------------
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
  - [X] 要建立一個機制可以輸入分隔的時間，自動將文字作時間分割處理
  - [X] 要將分析的設置變數拉出來
---------------------------------------
#### 2017/01/09
* 將各主題的時間開頭時間對齊做分析，門檻0.5, 結果在20180109_result.txt中
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