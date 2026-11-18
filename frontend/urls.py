from django.urls import path
from .views import FrontendIndexView, FrontendDetailView, FrontendLoginView, FrontendProfileView, FrontendUploadView, FrontendRegisterView

app_name = 'frontend'

urlpatterns = [
    path('', FrontendIndexView.as_view(), name='index'),

    path('photo/<int:pk>/', FrontendDetailView.as_view(), name='detail'), 

    path('login/', FrontendLoginView.as_view(), name='login'),

    path('profile/', FrontendProfileView.as_view(), name='profile'),

    path('upload/', FrontendUploadView.as_view(), name='upload'),

    path('register/', FrontendRegisterView.as_view(), name='register')
]