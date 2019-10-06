# -*- coding: utf-8 -*-
from . import text_rank as tr
#import transcribe_streaming_mic as tsm
import os
import json
import glob

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
    def __init__(self):
        self.speech_list = []
        self.all_text = ""

    def sum_json_file(self, dirname):
        self.speech_list=[]
        for filename in glob.glob(dirname+"voicetext*.json"):
            with open(filename, encoding="UTF-8-sig") as json_file:
                json_data = json.load(json_file)
                for j in json_data["data"] :
                    self.speech_list.append({'name':json_data["name"], "time":j["indata"]["time"],
                                "text":j["indata"]["text"],'state':"default",'percent':0})
        self.speech_list = sorted(self.speech_list, key=lambda k: k["time"])

        return self.speech_list

    def all_text_merge(self):
        for s in self.speech_list:
            self.all_text += (" " + s["text"].strip())

    def get_text(self):
        return self.all_text

    def data_summarize(self, number_of_summarize):
        try:
            rank = tr.TextRank(self.all_text)
            self.result = rank.summarize(number_of_summarize)
        except:
            self.result = "cannot summarization"
        return self.result

    def data_keywords(self, number_of_keywords):
        try:
            ky = tr.TextRank(self.all_text)
            self.key_result = ky.keywords(number_of_keywords)
        except:
            self.key_result = []
        return self.key_result
