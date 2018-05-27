# -*- coding: utf-8 -*-
# @Time    : 2018/3/24 下午 12:58
# @Author  : Yuhsuan
# @File    : mainpath_textrank_summary.py
# @Software: PyCharm

# pip install summa
import os
from summa import summarizer

import os
from shutil import copyfile


# 建立wiki上的比對檔案並複製到特定的資料夾
def reference_file(file_group, task_number, sim_type, i):
    ref = ["brexit", "missile", "brexit", "brexit", "brexit", "brexit", "catalan", "catalan", "crimea", "crimea",
           "gravitational", "gravitational", "brexit", "hk", "catalan", "sewol", "syria", "syria", "turkish"]

    wiki_file = ref[file_group]
    if not os.path.exists("textrank/{sim_type}/reference".format(sim_type=sim_type)):
        os.mkdir("textrank/{sim_type}/reference".format(sim_type=sim_type))

    source = "wiki/{wiki_file}.txt".format(wiki_file=wiki_file)
    destination = "textrank/{sim_type}/reference/task{task_number}_group{file_group}th{i}.txt".format(
        task_number=task_number,
        sim_type=sim_type,
        file_group=file_group,
        i=i)
    copyfile(source, destination)


if not os.path.exists("textrank"):
    os.mkdir("textrank")

for sim_type in ["tf_pdf", "tf_idf", "simple"]:
    task = 1
    for file_group in range(19):
        for i in range(1, 100):
            source = "main_path_summary/{sim_type}/{file_group}_{i}.txt".format(sim_type=sim_type,
                                                                                file_group=file_group,
                                                                                i=i)

            if not os.path.exists("textrank/{sim_type}".format(sim_type=sim_type)):
                os.mkdir("textrank/{sim_type}".format(sim_type=sim_type))

            if not os.path.exists("textrank/{sim_type}/system".format(sim_type=sim_type)):
                os.mkdir("textrank/{sim_type}/system".format(sim_type=sim_type))

            if os.path.exists(source):
                text = ""
                with open(source, "r", encoding="utf8") as file:
                    text = file.read()

                textrank = summarizer.summarize(text)

                with open("textrank/{sim_type}/system/task{task}_group{file_group}th{i}.txt"
                                  .format(sim_type=sim_type,
                                          task=task,
                                          file_group=file_group,
                                          i=i), "w",
                          encoding="utf8") as file:
                    file.write(textrank)
                reference_file(file_group, task, sim_type, i)
                task = task + 1
