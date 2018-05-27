# -*- coding: utf-8 -*-
# @Time    : 2018/4/14 下午4:39
# @Author  : yu_hsuan_chen@trend.com.tw
# @File    : rouge_file_transformer
# @Version : 3.6

import os
from shutil import copyfile


# 建立系統產生的檔案並複製到特定資料夾
def system_file():
    for sim_type in ["tf_pdf", "tf_idf", "simple"]:
        task_number = 1
        # 檢查目標路徑是否存在
        if not os.path.exists("main_path_summary/system/%s" % sim_type):
            os.mkdir("main_path_summary/system/%s" % sim_type)

        if not os.path.exists("main_path_summary/reference/%s" % sim_type):
            os.mkdir("main_path_summary/reference/%s" % sim_type)

        for file_group in range(19):
            for i in range(1, 100):
                source = "main_path_summary/{sim_type}/{file_group}_{i}.txt".format(sim_type=sim_type,
                                                                                    file_group=file_group,
                                                                                    i=i)
                destination = "main_path_summary/system/{sim_type}/task{task_number}_group{file_group}th{i}.txt".format(
                    task_number=task_number,
                    sim_type=sim_type,
                    file_group=file_group,
                    i=i)
                # 確認有檔案才複製
                if os.path.exists(source):
                    print(source, destination)
                    copyfile(source, destination)
                    reference_file(file_group, task_number, sim_type, i)
                    task_number = task_number + 1


# 建立wiki上的比對檔案並複製到特定的資料夾
def reference_file(file_group, task_number, sim_type, i):
    ref = ["brexit", "missile", "brexit", "brexit", "brexit", "brexit", "catalan", "catalan", "crimea", "crimea",
           "gravitational", "gravitational", "brexit", "hk", "catalan", "sewol", "syria", "syria", "turkish"]

    wiki_file = ref[file_group]
    source = "wiki/{wiki_file}.txt".format(wiki_file=wiki_file)
    destination = "main_path_summary/reference/{sim_type}/task{task_number}_group{file_group}th{i}.txt".format(
        task_number=task_number,
        sim_type=sim_type,
        file_group=file_group,
        i=i)
    copyfile(source, destination)


def main():
    system_file()


if __name__ == "__main__":
    main()
