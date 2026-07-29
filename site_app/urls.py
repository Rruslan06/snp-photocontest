
from django.urls import path

from site_app import views

app_name = "site_app" #Пространство имен ссылок, чтобы потом использовать в связке с name и не хардкордить шаблоны

urlpatterns = [
    #http:127.0.0.1:8000/
    path('', views.PhotoListView.as_view(), name='master_page'),

    #http:127.0.0.1:8000/photo/номер PK
    path('photo/<int:pk>/', views.PhotoDetailView.as_view(), name='detail_page'),

    #http:127.0.0.1:8000/profile/
    path('profile/', views.UserProfileView.as_view(), name='profile'),

    #http:127.0.0.1:8000/upload/
    path('upload/', views.PhotoCreateView.as_view(), name='photo_upload'),

    #http:127.0.0.1:8000/photo/номер PK/comment
    path('/<int:pk>/comment/', views.add_comment, name="add_comment"),

    #http:127.0.0.1:8000/photo/номер PK/comment
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    #http:127.0.0.1:8000/photo/номер PK/vote
    path('photo/<int:pk>/vote/', views.toggle_vote, name="toggle_vote")

]
