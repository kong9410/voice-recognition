from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('api/load', views.load, name='load'),
    path('result', views.result, name='result'),
    path('',views.main),
    path('login_ok',views.login_ok),
    path('content',views.content),
    path('detail_analysis',views.detail_analysis),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)