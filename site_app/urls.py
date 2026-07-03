
from django.urls import path

from site_app import views

app_name = "site_app" #Пространство имен ссылок, чтобы потом использовать в связке с name и не хардкордить шаблоны

urlpatterns = [
    #http:127.0.0.1:8000/
    path('', views.PhotoListView.as_view(), name='master_page'),

    #http:127.0.0.1:8000/photo/номер PK
    path('photo/<int:pk>/', views.PhotoDetailView.as_view(), name='detail_page'),

]
