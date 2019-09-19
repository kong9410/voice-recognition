# -*- coding: utf-8 -*-

import text_rank as tr
#import transcribe_streaming_mic as tsm
import os

class voice_json:
    def search(dirname):
        filenames = os.listdir(dirname)
        return filenames
    def fileopen(dirname, filename):
        with open(dirname + filename, 'r', encoding='utf8') as f:
            data = f.read()
            return data


if __name__ == "__main__":
    # 파일 불러오기
    vj = voice_json
    dirname = "./src/text/"
    filenames = vj.search(dirname)
    print(filenames[0])

    text = filenames[0]
    rank = tr.TextRank(text)
    print(rank.summarize(2))
    #with open(dirname+)