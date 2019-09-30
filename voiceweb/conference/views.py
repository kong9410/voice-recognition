from django.shortcuts import render
# import text_rank
from . import read_analysis as ras
import os
from . import transcribe_streaming_mic
# Create your views here.

# Create your views here.
def main(request):
    return render(request, 'vw/main.html')

def conference_analysis(request):
    vj = ras.voice_json
    dirname = "./conference/src/text/"
    filenames = vj.search(dirname)
    data = vj.fileopen(dirname, filenames[0])
    ra = ras.read_analysis(data)
    result = ra.data_summarize(4)
    keywords = ra.data_keywords(10)
    print(keywords)
    context = {
        "summarize" : result,
        "keywords" : keywords,
    }
    return render(request, 'vw/main.html', context=context)


def index(request):
    return render(request, 'vw/index.html')


def voice_input_start(requset):
    #name을 index에서 입력받아서 넘겨줘야함
    name=0
    if requset.method == 'POST':
        name = requset.POST["name_field"]
        print(name)
    transcribe_streaming_mic.main(name)
    return render(requset, 'vw/index.html')
