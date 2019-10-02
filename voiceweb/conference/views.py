from django.shortcuts import render
# import text_rank
from . import read_analysis as ras
import os
import json
from . import transcribe_streaming_mic
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


def index(request):
    return render(request, 'vw/index.html')


def voice_input_start(requset):
    name=0
    if requset.method == 'POST':
        name = requset.POST["name_field"]
    transcribe_streaming_mic.main(name)
    with open('voicetext.json', encoding="UTF-8-sig") as json_file:
        json_data = json.load(json_file)
        json_name = json_data["name"]
        json_time=[]
        json_text=[]

        for j in json_data["data"] :
         json_time.append(json_name)
         json_time.append(j["indata"]["time"])
         json_time.append(j["indata"]["text"])
        context = {
            "data" : json_time
        }
    return render(requset, 'vw/resultpage.html', context)