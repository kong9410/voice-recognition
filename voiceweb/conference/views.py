from django.shortcuts import render
# import text_rank
from . import read_analysis as ras
import os
import glob
import json
from . import transcribe_streaming_mic

# 감성 분석 모델 관련 패키지##########
from tensorflow.keras import models
from tensorflow.keras.models import load_model
import json
import os
from pprint import pprint
from konlpy.tag import Okt
import numpy as np
import nltk
############전역변수#######################
model = load_model('sentimental/meeting_mlp_model.h5')

if os.path.isfile('sentimental/train_docs.json'):
        with open('sentimental/train_docs.json', encoding='utf-8') as f:
            train_docs = json.load(f)
okt = Okt()
selected_words=[]
###################################


# Create your views here.

# Create your views here.
def main(request):
    return render(request, 'vw/main.html')

def conference_analysis(request):
    context={
        "summarize":"test",
        "keywords":"test",
    }
    # vj = ras.voice_json
    # dirname = "./conference/src/text/"
    # filenames = vj.search(dirname)
    # data = vj.fileopen(dirname, filenames[0])
    # ra = ras.read_analysis(data)
    # result = ra.data_summarize(4)
    # keywords = ra.data_keywords(10)
    # print(keywords)
    # context = {
    #     "summarize" : result,
    #     "keywords" : keywords,
    # }
    return render(request, 'vw/main.html', context=context)


def record(request):
    return render(request, 'vw/index.html')


def voice_input_start(requset):
    name=0
    if requset.method == 'POST':
        name = requset.POST["name_field"]
    transcribe_streaming_mic.main(name)
    return render(requset, 'vw/index.html')

def upload(request):
    return render(request, 'vw/upload.html')

def login_ok(request):
    if request.method == 'POST':
        name = request.POST['name']
        print(name)
    
    return render(request, 'vw/login_ok.html')

def content(request):
    sentimental_analysis()
    return render(request, 'vw/content.html')


def detail_analysis(request):
    return render(request, 'vw./detail_analysis.html')

################# 감성 분석 모델 관련 함수##################

def tokenize(doc):
    global okt
    # norm은 정규화, stem은 근어로 표시하기를 나타냄
    return ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True)]




def term_frequency(doc):
    global selected_words
    return [doc.count(word) for word in selected_words]


def predict_pos_neg(opinion):
    global okt
    global selected_words
    token = tokenize(opinion)
    tf = term_frequency(token)
    data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)
    global model
    score = model.predict(data)
    max_index=0
    max_value=-1
    index=0
    for prob in score[0]:
        if max_value< prob:
            max_value=prob
            max_index=index
        index+=1
    if max_index==0:
        print("[{}]는 {:.2f}% 확률로 부정 리뷰이지 않을까 추측해봅니다.^^\n".format(opinion, max_value * 100))
    elif max_index==1:
        print("[{}]는 {:.2f}% 확률로 중립 리뷰이지 않을까 추측해봅니다.^^\n".format(opinion, max_value * 100))
    elif max_index==2:
        print("[{}]는 {:.2f}% 확률로 긍정 리뷰이지 않을까 추측해봅니다.^^\n".format(opinion, max_value * 100))

def sentimental_analysis():
    global model
    global train_docs
    global okt
    global selected_words
    model = load_model('sentimental/meeting_mlp_model.h5') # 감성 분석 모델
    if os.path.isfile('sentimental/train_docs.json'):
        with open('sentimental/train_docs.json', encoding='utf-8') as f:
            train_docs = json.load(f) 

    tokens = [t for d in train_docs for t in d[0]]
    text = nltk.Text(tokens, name='NMSC')
    selected_words = [f[0] for f in text.vocab().most_common(4500)]
    predict_pos_neg("내일 공강이다.")


################# 감성 분석 모델 관련 함수##################

def sum_json_file(request):
    json_name = []
    json_time = []
    json_text = []
    list=[]
    for filename in glob.glob("voicetext*.json"):
     with open(filename, encoding="UTF-8-sig") as json_file:
        json_data = json.load(json_file)
        for j in json_data["data"] :
         list.append({'name':json_data["name"], "time":j["indata"]["time"],
                      "text":j["indata"]["text"]})
    list= sorted(list,key=lambda k:k["time"])
    print(list)
