import os
import pandas as pd
from shutil import copyfile


class copy_file:

    def __init__(self):
        self.NEWS_EVENT = ["brexit","missile","brexit","brexit","brexit","brexit","catalan","catalan","crimea","crimea","gravitational","gravitational","brexit","hk","catalan","sewol","syria","syria","turkish"]
        self.FOLDER = os.path.dirname(__file__)

    # task_englishReference.txt
    def process_lexrank(self):
        if not os.path.exists("lexrank/reference"):
            os.mkdir("lexrank/reference")

        if not os.path.exists("lexrank/system"):
            os.mkdir("lexrank/system")

        for group_name in range(19):
            copyfile(self.FOLDER+"/lexrank/%s.text" % group_name, self.FOLDER+"/lexrank/system/task%s_englishSyssum1.txt" % str(group_name))

        group_number = 0
        for i in self.NEWS_EVENT:
            copyfile("wiki/%s.txt" % i,"lexrank/reference/task%s_englishReference1.txt" % group_number)
            group_number=group_number+1

    def process_mainpath(self):
        if not os.path.exists("main_path_summary/reference"):
            os.mkdir("main_path_summary/reference")

        if not os.path.exists("main_path_summary/system"):
            os.mkdir("main_path_summary/system")

        task = 1
        for group_name in range(19):
            for i in range(1,100):
                if os.path.exists("main_path_summary/%s_%s.txt" % (group_name,i)):
                    copyfile("main_path_summary/%s_%s.txt" % (group_name, i), "main_path_summary/system/task%s_group%sth%s.txt" % (task, group_name, i))

                    copyfile("wiki/%s.txt" % self.NEWS_EVENT[group_name], "main_path_summary/reference/task%s_group%sth%s.txt" % (task, group_name, i))

                    task = task+1

    def process_textrank(self):
        if not os.path.exists("textrank/reference"):
            os.mkdir("textrank/reference")

        if not os.path.exists("textrank/system"):
            os.mkdir("textrank/system")

        task = 1
        for group_name in range(19):
            for i in range(1,100):
                if os.path.exists("textrank/%s_%s.txt" % (group_name,i)):
                    copyfile("textrank/%s_%s.txt" % (group_name, i), "textrank/system/task%s_group%sth%s.txt" % (task, group_name, i))

                    copyfile("wiki/%s.txt" % self.NEWS_EVENT[group_name], "textrank/reference/task%s_group%sth%s.txt" % (task, group_name, i))

                    task = task+1


class report():

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


if __name__ == "__main__":
    # cp = copy_file()
    # cp.process_lexrank()
    # cp.process_mainpath()
    # cp.process_textrank()
    report = report()
    # report.textrank()
    report.mainpath()
    pass