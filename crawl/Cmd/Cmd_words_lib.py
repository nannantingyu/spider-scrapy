# -*- coding: utf-8 -*-
import sys, os
reload(sys)
sys.setdefaultencoding('utf-8')
from crawl.settings import DATA_DIR

class CmdWordsLib:
    def __init__(self):
        self.words_lib_path = os.path.join(DATA_DIR, "user_dict.txt")

    def start(self):
        words = set()
        with open(self.words_lib_path, "r") as fs:
            while True:
                line = fs.readline().replace("\n", "")
                if line:
                    words.add(line)
                else:
                    break

        print len(words)
        with open(self.words_lib_path, "w") as fs:
            fs.write("\n".join(words))

        print "去重成功".encode('gbk')