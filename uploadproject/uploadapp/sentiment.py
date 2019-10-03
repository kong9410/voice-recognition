# 감성 분석 모델 관련 패키지##########
from tensorflow.keras import models
from tensorflow.keras.models import load_model
import json
import os
from pprint import pprint
from konlpy.tag import Okt
import numpy as np
import nltk
from . import read_analysis
############전역변수#######################

class sentiment:
    def __init__(self):
        self.model = load_model('sentimental/meeting_mlp_model.h5')

        if os.path.isfile('sentimental/train_docs.json'):
                with open('sentimental/train_docs.json', encoding='utf-8') as f:
                    self.train_docs = json.load(f)
        self.okt = Okt()
        self.selected_words=[]
        self.list = []
###################################
################# 감성 분석 모델 관련 함수##################

    def tokenize(self, doc):
        # norm은 정규화, stem은 근어로 표시하기를 나타냄
        return ['/'.join(t) for t in self.okt.pos(doc, norm=True, stem=True)]

    def term_frequency(self, doc):
        return [doc.count(word) for word in self.selected_words]


    def predict_pos_neg(self, opinion):
        token = self.tokenize(opinion)
        tf = self.term_frequency(token)
        data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)
        score = self.model.predict(data)
        max_index=0
        max_value=-1
        index=0
        for prob in score[0]:
            if max_value< prob:
                max_value=prob
                max_index=index
            index+=1
        if max_index==0:
            # print("[{}]는 {:.2f}% 확률로 부정 리뷰이지 않을까 추측해봅니다.^^\n".format(opinion, max_value * 100))
            state = "부정"
        elif max_index==1:
            # print("[{}]는 {:.2f}% 확률로 중립 리뷰이지 않을까 추측해봅니다.^^\n".format(opinion, max_value * 100))
            state = "중립"
        elif max_index==2:
            # print("[{}]는 {:.2f}% 확률로 긍정 리뷰이지 않을까 추측해봅니다.^^\n".format(opinion, max_value * 100))
            state = "긍정"
        return state, int(max_value*100)

    def sentimental_analysis(self):
        self.model = load_model('sentimental/meeting_mlp_model.h5') # 감성 분석 모델
        if os.path.isfile('sentimental/train_docs.json'):
            with open('sentimental/train_docs.json', encoding='utf-8') as f:
                train_docs = json.load(f)
        ras=read_analysis.read_analysis()
        dirname = 'media\\2019-10-03\\'
        self.list= ras.sum_json_file(dirname=dirname)
        ras.all_text_merge()
        text=ras.get_text()

        tokens = [t for d in self.train_docs for t in d[0]]
        text = nltk.Text(tokens, name='NMSC')
        self.selected_words = [f[0] for f in text.vocab().most_common(4500)]
        for i in range(0,len(self.list)) :
            state, percent= self.predict_pos_neg(self.list[i]['text'])
            self.list[i].update({'state':state,'percent':percent})
    
    def get_list(self):
        return self.list

