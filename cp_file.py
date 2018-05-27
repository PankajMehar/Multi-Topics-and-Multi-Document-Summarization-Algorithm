import os
import pandas as pd
from shutil import copyfile
import json
import re


class copy_file:

    def __init__(self):
        self.NEWS_EVENT = ["brexit", "missile", "brexit", "brexit", "brexit", "brexit", "catalan", "catalan", "crimea",
                           "crimea", "gravitational", "gravitational", "brexit", "hk", "catalan", "sewol", "syria",
                           "syria", "turkish"]
        self.FOLDER = os.path.dirname(__file__)

    # task_englishReference.txt
    def process_lexrank(self):
        if not os.path.exists("lexrank/reference"):
            os.mkdir("lexrank/reference")

        if not os.path.exists("lexrank/system"):
            os.mkdir("lexrank/system")

        for group_name in range(19):
            copyfile(self.FOLDER + "/lexrank/%s.text" % group_name,
                     self.FOLDER + "/lexrank/system/task%s_englishSyssum1.txt" % str(group_name))

        group_number = 0
        for i in self.NEWS_EVENT:
            copyfile("wiki/%s.txt" % i, "lexrank/reference/task%s_englishReference1.txt" % group_number)
            group_number = group_number + 1

    def process_mainpath(self):
        if not os.path.exists("main_path_summary/reference"):
            os.mkdir("main_path_summary/reference")

        if not os.path.exists("main_path_summary/system"):
            os.mkdir("main_path_summary/system")

        task = 1
        for group_name in range(19):
            for i in range(1, 100):
                if os.path.exists("main_path_summary/%s_%s.txt" % (group_name, i)):
                    copyfile("main_path_summary/%s_%s.txt" % (group_name, i),
                             "main_path_summary/system/task%s_group%sth%s.txt" % (task, group_name, i))

                    copyfile("wiki/%s.txt" % self.NEWS_EVENT[group_name],
                             "main_path_summary/reference/task%s_group%sth%s.txt" % (task, group_name, i))

                    task = task + 1

    def process_textrank(self):
        if not os.path.exists("textrank/reference"):
            os.mkdir("textrank/reference")

        if not os.path.exists("textrank/system"):
            os.mkdir("textrank/system")

        task = 1
        for group_name in range(19):
            for i in range(1, 100):
                if os.path.exists("textrank/%s_%s.txt" % (group_name, i)):
                    copyfile("textrank/%s_%s.txt" % (group_name, i),
                             "textrank/system/task%s_group%sth%s.txt" % (task, group_name, i))

                    copyfile("wiki/%s.txt" % self.NEWS_EVENT[group_name],
                             "textrank/reference/task%s_group%sth%s.txt" % (task, group_name, i))

                    task = task + 1


class report:

    def __init__(self):
        pass

    def mainpath(self):
        df = pd.read_csv("main_path_summary/temp.csv")
        res = []
        for i in range(19):
            df2 = df.loc[df['GROUP'] == i]
            df2 = df2.loc[df['ROUGE-Type'] == 'ROUGE-L+StopWordRemoval']
            df2 = df2['Avg_Recall']
            res.append(list(df2))
        # print(res)
        result = pd.DataFrame(res).transpose()
        result.to_csv("main_path_summary/temp_result.csv")

    def textrank(self):
        df = pd.read_csv("textrank/temp.csv")
        res = []
        for i in range(19):
            df2 = df.loc[df['GROUP'] == i]
            df2 = df2.loc[df['ROUGE-Type'] == 'ROUGE-L+StopWordRemoval']
            df2 = df2['Avg_Recall']
            res.append(list(df2))
        # print(res)
        result = pd.DataFrame(res).transpose()
        result.to_csv("textrank/temp_result.csv")

    # /Users/yu_hsuan_chen/Desktop/rouge/main_path_simple.csv

    def all(self):
        file_path = ["/Users/yu_hsuan_chen/Desktop/rouge/main_path_simple.csv",
                     "/Users/yu_hsuan_chen/Desktop/rouge/main_path_tf_idf.csv",
                     "/Users/yu_hsuan_chen/Desktop/rouge/main_path_tf_pdf.csv",
                     "/Users/yu_hsuan_chen/Desktop/rouge/textrank_simple.csv",
                     "/Users/yu_hsuan_chen/Desktop/rouge/textrank_tf_idf.csv",
                     "/Users/yu_hsuan_chen/Desktop/rouge/textrank_tf_pdf.csv",
                     "/Users/yu_hsuan_chen/Desktop/rouge/lexrank_tf_pdf.csv"]

        # file_path = ["/Users/yu_hsuan_chen/Desktop/rouge/lexrank_tf_pdf.csv"]

        rouge_type = ["ROUGE-1+StopWordRemoval","ROUGE-2+StopWordRemoval","ROUGE-L+StopWordRemoval","ROUGE-SU4+StopWordRemoval"]
        verify_rate = ["Avg_Recall","Avg_Precision","Avg_F-Score"]
        for rouge in range(len(rouge_type)):
            for rate in verify_rate:
                for path in file_path:
                    df = pd.read_csv(path)
                    res = []
                    for i in range(19):
                        df2 = df.loc[df['GROUP'] == str(i)]
                        df2 = df2.loc[df['ROUGE-Type'] == rouge_type[rouge]]
                        df2 = df2[rate]
                        res.append(list(df2))
                    result = pd.DataFrame(res).transpose()
                    newpath = path.replace(".csv", "_%s_%s.csv" % (rouge,rate))
                    result.to_csv(newpath)

    def fix(self):
        file_path = ["/Users/yu_hsuan_chen/Desktop/Rouge_Final/LexRank_TFPDF.csv",
                     "/Users/yu_hsuan_chen/Desktop/Rouge_Final/MainPath_Simple_TextRank.csv",
                     "/Users/yu_hsuan_chen/Desktop/Rouge_Final/MainPath_Simple.csv",
                     "/Users/yu_hsuan_chen/Desktop/Rouge_Final/MainPath_TFIDF_TextRank.csv",
                     "/Users/yu_hsuan_chen/Desktop/Rouge_Final/MainPath_TFIDF.csv",
                     "/Users/yu_hsuan_chen/Desktop/Rouge_Final/MainPath_TFPDF_TextRank.csv",
                     "/Users/yu_hsuan_chen/Desktop/Rouge_Final/MainPath_TFPDF.csv",
                     "/Users/yu_hsuan_chen/Desktop/Rouge_Final/TextRank.csv",
                     ]
        file_path=["/Users/yu_hsuan_chen/Desktop/rouge2-1.0-distribute/results.csv"]
        for file in file_path:
            df = pd.read_csv(file)
            df = pd.DataFrame(df)
            out = df.to_json(orient="values")
            temp = list(json.loads(out))

            db = []

            for item in temp:
                temp2 = list(item)
                if temp2[2] !="STORE":
                    res = re.match(re.compile("GROUP(\d+)TH(\d+)"),temp2[2])
                    group = res.group(1)
                    th = res.group(2)
                    temp2.append(int(group))
                    temp2.append(int(th))
                    print(temp2)
                    db.append(temp2)

            verify_rate = ["Recall", "Precision", "FScore"]
            for rate in range(len(verify_rate)):
                res = []
                for group in range(19):
                    temp = []
                    for th in range(1, 100):
                        for item in db:
                            if item[7] == group and item[8] == th and item[0] =="ROUGE-1+StopWordRemoval":
                                temp.append(item[rate+3])
                    res.append(temp)

                df = pd.DataFrame(res).transpose()
                df.to_csv(file.replace(".csv", "_%s.csv" % verify_rate[rate]))


if __name__ == "__main__":
    report = report()
    report.fix()
