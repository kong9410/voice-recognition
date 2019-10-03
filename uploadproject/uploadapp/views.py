from django.shortcuts import render
from .forms import UploadFileForm
from .models import UploadFileModel
# Create your views here.

def index(request):
    return render(request, 'index.html')
    
def load(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('files') #field name in model
        if form.is_valid():
            for f in files:
                file_instance = UploadFileModel(files=f)
                file_instance.save()
        else:
            print('load failed')
        
        return render(request, 'load.html', {'form':form})
    
def result(request):
    return render(request, 'result.html')


def login_ok(request):
    if request.method == 'POST':
        name = request.POST['name']
        print(name)
    
    return render(request, 'login_ok.html')

def content(request):
    sentimental_analysis()
    print(list)
    """
    context={
        "data" : list,
        "loop_times" : range(0,len(list)),
    }
    """

    return render(request, 'content.html',{"list":list})


def detail_analysis(request):
    return render(request, 'detail_analysis.html')

def main(request):
    return render(request, 'main.html')



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


model = load_model('sentimental/meeting_mlp_model.h5')

if os.path.isfile('sentimental/train_docs.json'):
        with open('sentimental/train_docs.json', encoding='utf-8') as f:
            train_docs = json.load(f)
okt = Okt()
selected_words=[]
###################################
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
    state=""
    for prob in score[0]:
        if max_value< prob:
            max_value=prob
            max_index=index
        index+=1
    if max_index==0:
        print("[{}]는 {:.2f}% 확률로 부정 리뷰이지 않을까 추측해봅니다.^^\n".format(opinion, max_value * 100))
        state="부정"
    elif max_index==1:
        print("[{}]는 {:.2f}% 확률로 중립 리뷰이지 않을까 추측해봅니다.^^\n".format(opinion, max_value * 100))
        state="중립"
    elif max_index==2:
        print("[{}]는 {:.2f}% 확률로 긍정 리뷰이지 않을까 추측해봅니다.^^\n".format(opinion, max_value * 100))
        state="긍정"
    return state, int(max_value*100)
def sentimental_analysis():
    global model
    global train_docs
    global okt
    global selected_words
    model = load_model('sentimental/meeting_mlp_model.h5') # 감성 분석 모델
    if os.path.isfile('sentimental/train_docs.json'):
        with open('sentimental/train_docs.json', encoding='utf-8') as f:
            train_docs = json.load(f)
    ras=read_analysis.read_analysis()
    dirname = 'media\\2019-10-03\\'
    global list
    list= ras.sum_json_file(dirname=dirname)
    ras.all_text_merge()
    text=ras.get_text()

    tokens = [t for d in train_docs for t in d[0]]
    text = nltk.Text(tokens, name='NMSC')
    selected_words = [f[0] for f in text.vocab().most_common(4500)]
    for i in range(0,len(list)) :
     a,b= predict_pos_neg(list[i]['text'])
     list[i].update({'state':a,'percent':b})
     print(list[i])

