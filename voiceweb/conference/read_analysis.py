# -*- coding: utf-8 -*-

from . import text_rank as tr
#import transcribe_streaming_mic as tsm
import os
import json

class voice_json:
    def search(dirname):
        print(os.listdir('.'))
        filenames = os.listdir(dirname)
        return filenames
    def fileopen(dirname, filename):
        with open(dirname + filename, 'r', encoding='utf8') as f:
            data = json.load(f)
            return data

class read_analysis:
    def __init__(self, data):
        ler = int(len(data['data']))
        self.all_text = ""
        for elem in data['data']:
            time = elem['indata']['time']
            text = elem['indata']['text'].strip()
            self.all_text = self.all_text + " " + text
        self.all_text = self.all_text.strip()
        self.result = "None"
    def get_text(self):
        return self.all_text
    def data_summarize(self, number_of_summarize):
        try:
            rank = tr.TextRank(self.all_text)
            self.result = rank.summarize(number_of_summarize)
        except:
            self.result = "요약이 안됨"
        return self.result
    def data_keywords(self, number_of_keywords):
        try:
            ky = tr.TextRank(self.all_text)
            self.key_result = ky.keywords(number_of_keywords)
        except:
            self.key_result = []
        return self.key_result


if __name__ == "__main__":
    # 파일 불러오기
    vj = voice_json
    dirname = ".conference/src/text/"
    filenames = vj.search(dirname)
    print(filenames[0])
    data = vj.fileopen(dirname, filenames[0])
    ra = read_analysis(data)
    result = ra.data_summarize(0)
    print(result)

    