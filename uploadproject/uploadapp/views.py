from django.shortcuts import render
from .forms import UploadFileForm
from .models import UploadFileModel
from . import sentiment as stm
from . import read_analysis
from datetime import datetime
from collections import Counter
# Create your views here.

# 감성 분석 모델 관련 패키지##########
from tensorflow.keras import models
from tensorflow.keras.models import load_model
import json
import os
from pprint import pprint
from konlpy.tag import Okt
import numpy as np
import nltk
####################################
############전역변수#################
model = load_model('sentimental/meeting_mlp_model.h5')

if os.path.isfile('sentimental/train_docs.json'):
        with open('sentimental/train_docs.json', encoding='utf-8') as f:
            train_docs = json.load(f)
okt = Okt()
selected_words=[]
#####################################


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
        # 오늘 날짜로 폴더 찾기
    now = datetime.now()
    digital_month = str(now.month)
    if(now.month < 10):
        digital_month = "0"+digital_month
    digital_day = str(now.day)
    if(now.day < 10):
        digital_day = "0"+digital_day
    dirname = "media\\"+str(now.year)+"-"+digital_month+"-"+digital_day+"\\"

    sas = stm.sentiment()
    sas.sentimental_analysis(dirname)
    content_list = sas.get_list()
    return render(request, 'content.html',{"list":content_list})


def detail_analysis(request):
    # 오늘 날짜로 폴더 찾기
    now = datetime.now()
    digital_month = str(now.month)
    if(now.month < 10):
        digital_month = "0"+digital_month
    digital_day = str(now.day)
    if(now.day < 10):
        digital_day = "0"+digital_day
    dirname = "media\\"+str(now.year)+"-"+digital_month+"-"+digital_day+"\\"

    ras = read_analysis.read_analysis()
    speech_list = ras.sum_json_file(dirname)
    thetext = ras.all_text_merge()

    # 텍스트 요약    
    summarize_text = ras.data_summarize(4)
    import_keywords = ras.data_keywords(10)

    talker_list = set() # 회의 참여자
    list_of_talker = []
    speech_time = 0
    min_speech_time = 0xFFFFFF
    max_speech_time = 0
    for s in speech_list:
        talker_list.add(s["name"])
        list_of_talker.append(s["name"])
        max_speech_time = max(s["time"], max_speech_time)
        min_speech_time = min(s["time"], min_speech_time)
    
    #발화시간 계산
    speech_time = max_speech_time - min_speech_time
    speech_time = round(speech_time, 2)
    # talker_list = ['민철', '민재', '경민']
    talker_list = list(talker_list) # 발화자
    number_of_participants = len(talker_list) # 발화자 수
    # number_of_talker = Counter{"민철":20, "민재":30, "경민":24}
    number_of_talker = []
    for k, n in Counter(list_of_talker).items():
        number_of_talker.append(n)
    # number_of_talker = Counter(list_of_talker)  # 발화 수
    total_talk = 0
    for n in number_of_talker:
        total_talk += n

    sas = stm.sentiment()
    sas.sentimental_analysis(dirname)
    state_list = set()
    sentimental_list = sas.get_list()
    list_of_sent = []
    number_of_sentimental = []
    for s in sentimental_list:
        list_of_sent.append(s["state"])

    # number_of_sentimental = [80, 40, 60]
    for k, n in Counter(list_of_sent).items():
        number_of_sentimental.append(n)

    number_of_keywords = []
    for ls in import_keywords:
        number_of_keywords.append(ras.get_text().count(ls))

    context = {
        "summarize_text" : summarize_text,
        "import_keywords" : import_keywords,
        "number_of_keywords" : number_of_keywords,
        "talker_list" : talker_list,
        "number_of_talker" : number_of_talker,
        "total_talk" : total_talk,
        "number_of_sentimental" : number_of_sentimental,
        "speech_time" : speech_time,
        "number_of_participants" : number_of_participants,
    }
    print(context)
    return render(request, 'detail_analysis.html', context)

def main(request):
    return render(request, 'main.html')



# # 감성 분석 모델 관련 패키지##########
# from tensorflow.keras import models
# from tensorflow.keras.models import load_model
# import json
# import os
# from pprint import pprint
# from konlpy.tag import Okt
# import numpy as np
# import nltk
# from . import read_analysis
# ############전역변수#######################


# model = load_model('sentimental/meeting_mlp_model.h5')

# if os.path.isfile('sentimental/train_docs.json'):
#         with open('sentimental/train_docs.json', encoding='utf-8') as f:
#             train_docs = json.load(f)
# okt = Okt()
# selected_words=[]
# ###################################
# ################# 감성 분석 모델 관련 함수##################

# def tokenize(doc):
#     global okt
#     # norm은 정규화, stem은 근어로 표시하기를 나타냄
#     return ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True)]

# def term_frequency(doc):
#     global selected_words
#     return [doc.count(word) for word in selected_words]

# def predict_pos_neg(opinion):
#     global okt
#     global selected_words
#     token = tokenize(opinion)
#     tf = term_frequency(token)
#     data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)
#     global model
#     score = model.predict(data)
#     max_index=0
#     max_value=-1
#     index=0
#     state=""
#     for prob in score[0]:
#         if max_value< prob:
#             max_value=prob
#             max_index=index
#         index+=1
#     if max_index==0:
#         print("[{}]는 {:.2f}% 확률로 부정 리뷰이지 않을까 추측해봅니다.^^\n".format(opinion, max_value * 100))
#         state="부정"
#     elif max_index==1:
#         print("[{}]는 {:.2f}% 확률로 중립 리뷰이지 않을까 추측해봅니다.^^\n".format(opinion, max_value * 100))
#         state="중립"
#     elif max_index==2:
#         print("[{}]는 {:.2f}% 확률로 긍정 리뷰이지 않을까 추측해봅니다.^^\n".format(opinion, max_value * 100))
#         state="긍정"
#     return state, int(max_value*100)
# def sentimental_analysis():
#     global model
#     global train_docs
#     global okt
#     global selected_words
#     model = load_model('sentimental/meeting_mlp_model.h5') # 감성 분석 모델
#     if os.path.isfile('sentimental/train_docs.json'):
#         with open('sentimental/train_docs.json', encoding='utf-8') as f:
#             train_docs = json.load(f)
#     ras=read_analysis.read_analysis()
#     dirname = 'media\\2019-10-03\\'
#     global list
#     list= ras.sum_json_file(dirname=dirname)
#     ras.all_text_merge()
#     text=ras.get_text()

#     tokens = [t for d in train_docs for t in d[0]]
#     text = nltk.Text(tokens, name='NMSC')
#     selected_words = [f[0] for f in text.vocab().most_common(4500)]
#     for i in range(0,len(list)) :
#      a,b= predict_pos_neg(list[i]['text'])
#      list[i].update({'state':a,'percent':b})
#      print(list[i])

# from konlpy.tag import Twitter
# from collections import Counter

# def get_tags(text, ntags=50):
#     spliter = Twitter()
#     # konlpy의 Twitter객체
#     nouns = spliter.nouns(text)
#     # nouns 함수를 통해서 text에서 명사만 분리/추출
#     count = Counter(nouns)
#     # Counter객체를 생성하고 참조변수 nouns할당
#     return_list = []  # 명사 빈도수 저장할 변수
#     for n, c in count.most_common(ntags):
#         temp = {'tag': n, 'count': c}
#         return_list.append(temp)
#     # most_common 메소드는 정수를 입력받아 객체 안의 명사중 빈도수
#     # 큰 명사부터 순서대로 입력받은 정수 갯수만큼 저장되어있는 객체 반환
#     # 명사와 사용된 갯수를 return_list에 저장합니다.
#     return return_list