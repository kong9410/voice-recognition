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