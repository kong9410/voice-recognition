from django.shortcuts import render
from . import transcribe_streaming_mic
# Create your views here.
import os

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