from django.shortcuts import render
from .forms import UploadFileForm
from .models import UploadFileModel
from . import sentiment as stm
from . import text_rank
from . import read_analysis
from datetime import datetime
from collections import Counter
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
    sas = stm.sentiment()
    sas.sentimental_analysis()
    return render(request, 'content.html')


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
    for s in speech_list:
        talker_list.add(s["name"])
        list_of_talker.append(s["name"])

    # talker_list = ['민철', '민재', '경민']
    talker_list = list(talker_list) # 발화자
    
    # number_of_talker = {"민철":20, "민재":30, "경민":24}
    number_of_talker = Counter(list_of_talker)  # 발화 수

    sas = stm.sentiment()
    sas.sentimental_analysis()
    state_list = set()
    sentimental_list = sas.get_list()
    list_of_sent = []
    number_of_sentimental = []
    for s in sentimental_list:
        list_of_sent.append(s["state"])
    # number_of_sentimental = {"부정":80, "긍정":40, "중립":60}
    number_of_sentimental = Counter(list_of_sent) # 감정 수
    

    context = {
        "summarize_text" : summarize_text,
        "import_keywords" : import_keywords,
        "talker_list" : talker_list,
        "number_of_talker" : number_of_talker,
        "number_of_sentimental" : number_of_sentimental,
    }
    print(context)
    return render(request, 'detail_analysis.html', context)

def main(request):
    return render(request, 'main.html')


