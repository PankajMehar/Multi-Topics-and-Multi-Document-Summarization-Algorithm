# -*- coding: utf-8 -*-
# @Time    : 2018/5/4 下午6:34
# @Author  : yu_hsuan_chen@trend.com.tw
# @File    : retriver
# @Version : 3.6
import os

def main():
    FilePaths = ["/Users/yu_hsuan_chen/Desktop/摘要集/GroupCosineBase_LexRank",
                 "/Users/yu_hsuan_chen/Desktop/摘要集/GroupTFIDFBase_LexRank",
                 "/Users/yu_hsuan_chen/Desktop/摘要集/GroupTFPDF_LexRank",
                 "/Users/yu_hsuan_chen/Desktop/摘要集/GroupTFPDF_TextRank",
                 "/Users/yu_hsuan_chen/Desktop/摘要集/MainPath_Cosine",
                 "/Users/yu_hsuan_chen/Desktop/摘要集/MainPath_Cosine_TextRank",
                 "/Users/yu_hsuan_chen/Desktop/摘要集/MainPath_TFIDF",
                 "/Users/yu_hsuan_chen/Desktop/摘要集/MainPath_TFIDF_TextRank",
                 "/Users/yu_hsuan_chen/Desktop/摘要集/MainPath_TFPDF",
                 "/Users/yu_hsuan_chen/Desktop/摘要集/MainPath_TFPDF_TextRank",]

    for FilePath in FilePaths:
        SystemFilePath = FilePath+"/system/"
        FileLists = os.listdir(SystemFilePath)

        for file in FileLists:
            content = []
            file_path = os.path.join(SystemFilePath,file)
            with open(file_path, "r", encoding="utf8") as f:
                content = f.readlines()

            temp = ""
            for line in content:
                line = line.strip("\n")
                temp = temp + line

            print(temp)

            with open(file_path,"w",encoding="utf8") as f:
                f.write(temp)

if __name__ ==  "__main__":
    main()