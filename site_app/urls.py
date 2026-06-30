
from django.urls import path

from . import views

app_name = "site_app" #Пространство имен ссылок, чтобы потом использовать в связке с name и не хардкордить шаблоны

urlpatterns = [
    #http:127.0.0.1:8000/site_app/  ИЛИ #http:127.0.0.1:8000/
    path('', views.index, name='master_page'),

]
