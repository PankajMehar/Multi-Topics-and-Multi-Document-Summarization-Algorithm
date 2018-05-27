import json
import os
import re
from multiprocessing import Pool
from shutil import copyfile

from summa import summarizer
from datetime import datetime
import os


def reference_file(file_group, task, ratio):
    ref = ["brexit", "missile", "brexit", "brexit", "brexit", "brexit", "catalan", "catalan", "crimea", "crimea",
           "gravitational", "gravitational", "brexit", "hk", "catalan", "sewol", "syria", "syria", "turkish"]

    wiki_file = ref[file_group]

    source = "wiki/{wiki_file}.txt".format(wiki_file=wiki_file)
    destination = "textrank_simple/reference/task{task}_group{file_group}th{ratio}.txt".format(task=task,
                                                                                               file_group=file_group,
                                                                                               ratio=ratio)
    copyfile(source, destination)


def analyse_url(Tasks):
    try:
        print(str(datetime.now()) + " " + Tasks)
        res = re.match(re.compile("task(\d+)_group(\d+)th(\d+)"), Tasks)
        task = int(res[1])
        file_group = int(res[2])
        th = int(res[3])

        source = "group_data/{file_group}/group_{file_group}.json".format(file_group=file_group)
        dic = ""
        with open(source, "r", encoding="utf8") as file:
            group_data = json.load(file)
        dic = group_data

        content = ""
        for x in dic["source"]:
            content = content + dic["source"][x]
        ratio = th / 100
        textrank = summarizer.summarize(content, ratio=ratio)
        destination = "textrank_simple/system/task{task}_group{file_group}th{ratio}.txt".format(task=task,
                                                                                                file_group=file_group,
                                                                                                ratio=th)
        with open(destination, "w", encoding="utf8") as file:
            file.write(textrank)

        ref = ["brexit", "missile", "brexit", "brexit", "brexit", "brexit", "catalan", "catalan", "crimea", "crimea",
               "gravitational", "gravitational", "brexit", "hk", "catalan", "sewol", "syria", "syria", "turkish"]

        wiki_file = ref[file_group]

        source = "wiki/{wiki_file}.txt".format(wiki_file=wiki_file)
        destination = "textrank_simple/reference/task{task}_group{file_group}th{ratio}.txt".format(task=task,
                                                                                                   file_group=file_group,
                                                                                                   ratio=th)
        copyfile(source, destination)

        print(str(datetime.now()) + " " + Tasks + " Done.")
    except Exception as e:
        print("Find Exception in Tasks: {Tasks}\nException is: {Exception}".format(Tasks=Tasks, Exception=e))


def getFileList():
    path = "textrank_simple/system"
    FileLists = []
    for file in os.listdir(path):
        FileLists.append(file.replace(".txt", ""))
    print(len(FileLists))
    return FileLists


if __name__ == '__main__':
    paths = [
        "textrank_simple",
        "textrank_simple/reference",
        "textrank_simple/system"
    ]

    for path in paths:
        if not os.path.exists(path):
            os.mkdir(path)

    task = 1
    tasks = []
    for file_group in range(19):
        for ratio in range(1, 100):
            tasks.append("task{task}_group{file_group}th{ratio}".format(task=task, file_group=file_group, ratio=ratio))
            task = task + 1

    FileList = getFileList()

    # remove exists task

    for i in FileList:
        tasks.remove(i)

    print(len(tasks))
    print(os.cpu_count())

    # pool = Pool(os.cpu_count() - 1)
    # result = pool.map(analyse_url, tasks)
