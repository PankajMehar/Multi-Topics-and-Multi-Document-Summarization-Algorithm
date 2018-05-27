# -*- coding: utf-8 -*-
# @Time    : 2018/3/9 下午 05:01
# @Author  : Yuhsuan
# @File    : lexrank_summary.py
# @Software: PyCharm

from lexrank import STOPWORDS, LexRank
import os
import json
from log_module import log
import os
from shutil import copyfile

log("load reference doc")
documents = []
document_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bbc")

for dirPath, dirNames, fileNames in os.walk(document_dir):
    for f in fileNames:
        try:
            with open(os.path.join(dirPath, f), "rt", encoding="utf8") as file:
                documents.append(file.readlines())
        except Exception as e:
            log("path: %s%s" % (dirPath, f))

lxr = LexRank(documents, stopwords=STOPWORDS['en'])


# 建立wiki上的比對檔案並複製到特定的資料夾
def reference_file(file_group, task_number, sim_type, i):
    ref = ["brexit", "missile", "brexit", "brexit", "brexit", "brexit", "catalan", "catalan", "crimea", "crimea",
           "gravitational", "gravitational", "brexit", "hk", "catalan", "sewol", "syria", "syria", "turkish"]

    wiki_file = ref[file_group]
    if not os.path.exists("lexrank/{sim_type}/reference".format(sim_type=sim_type)):
        os.mkdir("lexrank/{sim_type}/reference".format(sim_type=sim_type))

    source = "wiki/{wiki_file}.txt".format(wiki_file=wiki_file)
    destination = "lexrank/{sim_type}/reference/task{task_number}_group{file_group}th{i}.txt".format(
        task_number=task_number,
        sim_type=sim_type,
        file_group=file_group,
        i=i)
    copyfile(source, destination)


for sim_type in ["tf_pdf", "tf_idf", "simple"]:
    task = 1
    for file_group in range(19):
        log(str(file_group))

        group_data = {}
        with open("group_data_%s/%s/group_%s.json" % (sim_type, file_group, file_group), "r", encoding="utf8") as file:
            group_data = json.load(file)

        sen = []
        for i in group_data["source"]:
            sen.append(group_data["source"][i])

        sentences = sen
        log("start summary")
        for i in range(1, 100):
            log("%s, %s, %s" % (sim_type,file_group,i))
            summary = lxr.get_summary(sentences, summary_size=10, threshold=(i / 100))
            # print(summary)
            if not os.path.exists("lexrank/{sim_type}/system".format(sim_type=sim_type)):
                os.mkdir("lexrank/{sim_type}/system".format(sim_type=sim_type))

            with open("lexrank/{sim_type}/system/task{task}_group{file_group}th{i}.text".format(sim_type=sim_type,
                                                                                                task=task,
                                                                                                file_group=file_group,
                                                                                                i=i), "w",
                      encoding="utf8") as file:
                file.writelines(summary)

            reference_file(file_group, task, sim_type, i)
            task = task + 1
