from django.shortcuts import render
# import text_rank
from . import read_analysis as ras
import os

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