from django.shortcuts import render, get_object_or_404 #Нужен чтобы использовать шаблоны(короткий путь) и ошибку 404

from django.urls import reverse #Как в шаблонах в Питоне используем удобную запись и не хардкордим страницу куда перейти

from django.views import generic #Чтобы использовать базовые представления(Generic View) 

from django.db.models import F #Чтобы работать с полями и не было состояния гонки

from django.http import HttpResponse, HttpResponseRedirect #Чтобы перенаправлять пользователя с POST на GET запросы(страницы)

from models_app.models import Photo, Comment
# Create your views here.


# def index(request):
#     photos = Photo.objects.all()
#     return render(request, "site_app/index.html", {"photos": photos})

class PhotoListView(generic.ListView):
    model = Photo
    template_name = 'site_app/index.html'
    context_object_name = 'photos'

    #Потом переопределить чтобы отображались только прошедшие модерацию
    def get_queryset(self):
        return super().get_queryset()



class PhotoDetailView(generic.DetailView):
    model = Photo #оснновная модель 
    template_name = 'site_app/detail.html'
    context_object_name = 'photo'

    def get_context_data(self, **kwargs):
        # Получаем стандартный контекст (в нем уже есть объект из ОсновнойМодели как 'object')
        context = super().get_context_data(**kwargs)
    
        context['comments'] = Comment.objects.filter(photo=self.object)

        return context