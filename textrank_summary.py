# -*- coding: utf-8 -*-
# @Time    : 2018/4/26 下午9:45
# @Author  : yu_hsuan_chen@trend.com.tw
# @File    : textrank_summary
# @Version : 3.6

import os
from summa import summarizer
from shutil import copyfile
import json
from log_module import log



def reference_file(file_group, task, ratio):
    ref = ["brexit", "missile", "brexit", "brexit", "brexit", "brexit", "catalan", "catalan", "crimea", "crimea",
           "gravitational", "gravitational", "brexit", "hk", "catalan", "sewol", "syria", "syria", "turkish"]

    wiki_file = ref[file_group]
    if not os.path.exists("textrank_simple/reference"):
        os.mkdir("textrank_simple/reference")

    source = "wiki/{wiki_file}.txt".format(wiki_file=wiki_file)
    destination = "textrank_simple/reference/task{task}_group{file_group}th{ratio}.txt".format(task=task,
                                                                                               file_group=file_group,
                                                                                               ratio=ratio)
    copyfile(source, destination)


def main():
    task = 1
    paths = [
        "textrank_simple",
        "textrank_simple/reference",
        "textrank_simple/system"
    ]

    for path in paths:
        if not os.path.exists(path):
            os.mkdir(path)

    for file_group in range(0,1):
        source = "group_data/{file_group}/group_{file_group}.json".format(file_group=file_group)
        # print(source)
        dic = ""
        with open(source, "r", encoding="utf8") as file:
            group_data = json.load(file)
        dic = group_data

        content = ""
        for x in dic["source"]:
            content = content + dic["source"][x]

        for i in range(1, 100):
            log("Task: {task}, FileGroup: {file_group}, i: {i}".format(task=task, file_group=file_group, i=i))
            print("summarize")
            ratio = i / 100
            textrank = summarizer.summarize(content, ratio=ratio)

            destination = paths[2] + "/task{task}_group{file_group}th{ratio}.txt".format(task=task,
                                                                                         file_group=file_group, ratio=i)

            with open(destination, "w", encoding="utf8") as file:
                file.write(textrank)

            reference_file(file_group, task, i)
            task = task + 1
            print("reference file done.")


if __name__ == "__main__":
    main()
    # 838 8 46
    # summarize
    # reference file done.
    # 839 8 47
    # summarize
