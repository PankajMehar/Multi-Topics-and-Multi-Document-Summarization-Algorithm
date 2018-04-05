# -*- coding: utf-8 -*-
# @Time    : 2018/3/8 下午 06:17
# @Author  : Yuhsuan
# @File    : Pajek.py
# @Software: PyCharm

import os
import re
import time
import subprocess


class pajek:
    def __init__(self, FILE_NAME, FOLDER=None, EXE_FILE=None):
        # 預設的Pajek的資料夾路徑
        if FOLDER == None:
            self.PAJEK_FORDER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pajek")
        else:
            self.PAJEK_FORDER_PATH = FOLDER

        # 預設的Pajek執行檔案路徑
        if EXE_FILE == None:
            self.EXE_FILE_PATH = os.path.join(self.PAJEK_FORDER_PATH, "Pajek.exe")
        else:
            self.EXE_FILE_PATH = EXE_FILE

        # 根據這個檔案名稱輸出所有相關的檔案
        self.FILE_NAME = FILE_NAME

        # 輸入的NET檔案路徑
        self.NET_FILE_PATH = os.path.join(self.PAJEK_FORDER_PATH, self.FILE_NAME + ".net")

        # 輸出的LOG檔案路徑
        self.LOG_PATH = os.path.join(self.PAJEK_FORDER_PATH, self.FILE_NAME + ".log")
        # 輸出的PAJ檔案路徑
        self.OUTPUT_PAJ = os.path.join(self.PAJEK_FORDER_PATH, self.FILE_NAME + ".paj")
        # 輸出的JPG檔案路徑
        self.OUTPUT_JPG = os.path.join(self.PAJEK_FORDER_PATH, self.FILE_NAME + ".jpg")
        # 最後的main_path
        self.MAIN_PATH = []

    def generate_log_file(self, NET_FILE_PATH, OUTPUT_PAJ, OUTPUT_JPG):
        LOG = """
        NETBEGIN 1
        CLUBEGIN 1
        PERBEGIN 1
        CLSBEGIN 1
        HIEBEGIN 1
        VECBEGIN 1

        % Reading Network   ---    {net_file_path}
        N 1 RDN "{net_file_path}" (203)
        % Weak Components
        C 1 COMP 1 [2] [1] (203)
        % Extracting Subnetwork according to Partition
        N 2 EXT 1 1 [1] 1 (151)
        % Strong Components
        C 3 COMP 2 [1] [1] (151)
        % Shrinking
        N 3 SHR 2 3 [1 ,0,1] (151)
        % Citation Weights: Search Path Count (SPC)
        V 3 CITSPC 3 0 1 (151)
        % Standard Global Main Path
        N 5 GLOBALMAINPATH 4 0 (13)
        E 5 CIRCULAR
        E 5 DRAW 0 0 0 0 0
        E 5 JPEG 0 0 0 0 0 "{output_jpg}" 100 0
        % Saving network to file   ---    {output_paj}
        % Saving network to file   ---    {output_paj}
        % Saving network to file   ---    {output_paj}
        % Saving network to file   ---    {output_paj}
        % Saving network to file   ---    {output_paj}
        % Saving partition to file   ---    {output_paj}
        % Saving partition to file   ---    {output_paj}
        % Saving partition to file   ---    {output_paj}
        % Saving partition to file   ---    {output_paj}
        % Saving partition to file   ---    {output_paj}
        % Saving vector to file   ---    {output_paj}
        % Saving vector to file   ---    {output_paj}
        % Saving vector to file   ---    {output_paj}
        N 9999 WRPAJ "{output_paj}"
        EXIT
        """.format(net_file_path=NET_FILE_PATH, output_paj=OUTPUT_PAJ, output_jpg=OUTPUT_JPG)

        self.LOG_PATH = os.path.join(self.PAJEK_FORDER_PATH, self.FILE_NAME + ".log")
        with open(self.LOG_PATH, "w", encoding='utf8') as file:
            file.write(LOG)

    def execute(self):
        cmd = "{exe} {log}".format(exe=self.EXE_FILE_PATH, log=self.LOG_PATH)
        # print(cmd)
        p = subprocess.Popen(cmd, shell=True)

    def analysis_main_path(self):
        data = []
        with open(self.OUTPUT_PAJ, "r", encoding="utf8") as file:
            data = file.readlines()

        line_start = 0
        line_end = 0

        # 找開始記錄main path的行數
        for start in range(len(data)):
            if "Network Standard Global Main Path" in data[start]:
                line_start = start + 2
                break

        # 找main path的最後一行
        for end in range(line_start, len(data)):
            if "Arcs" in data[end]:
                line_end = end - 1
                break
        # print(line_start,line_end)
        if line_start != 0:
            main_path = data[line_start:line_end + 1]

            # 處理main_path只剩下sg
            pattern = re.compile('.* \d+.* \"(.*)\".*')
            for i in range(len(main_path)):
                m = re.match(pattern, main_path[i])
                main_path[i] = m.group(1)
            self.MAIN_PATH = main_path
        else:
            return self.MAIN_PATH

    def _wait(self,file_path, sleeptime=None):
        if sleeptime == None:
            waite_time = 5
        else:
            waite_time = sleeptime

        for i in range(10):
            if not os.path.exists(file_path):
                time.sleep(waite_time)
            else:
                time.sleep(1)
                break

    def run(self):
        self.generate_log_file(self.NET_FILE_PATH, self.OUTPUT_PAJ, self.OUTPUT_JPG)
        # self._wait(self.LOG_PATH,2)
        time.sleep(3)
        self.execute()
        # self._wait(self.OUTPUT_PAJ)
        time.sleep(7)
        self.analysis_main_path()
        return self.MAIN_PATH

if __name__ == "__main__":
    p = pajek("25").run()
    print(p)