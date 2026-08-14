from django.shortcuts import render, get_object_or_404, redirect #Нужен чтобы использовать шаблоны(короткий путь) и ошибку 404

from django.urls import reverse #Как в шаблонах в Питоне используем удобную запись и не хардкордим страницу куда перейти

from django.views import generic #Чтобы использовать базовые представления(Generic View) 

from django.db.models import F #Чтобы работать с полями и не было состояния гонки

from django.http import HttpResponse, HttpResponseRedirect #Чтобы перенаправлять пользователя с POST на GET запросы(страницы)

from models_app.models import Photo, Comment, Vote

from django.db.models import Q # Q-объекты для гибких условий фильтрации

from django.contrib.auth.mixins import LoginRequiredMixin #Миксин для проверки что пользователь авторизован

from django.contrib.auth.decorators import login_required #Декоратор чтобы функиця проверяла что пользователь авторизован
# Create your views here.


class UserProfileView(LoginRequiredMixin, generic.ListView):
    model = Photo
    template_name = 'site_app/profile.html'
    context_object_name = 'photos'

    def get_queryset(self):
        # Достаем фото только того пользователя, который сейчас залогинен
        queryset = Photo.objects.filter(author=self.request.user).order_by('-date')
        status_param = self.request.GET.get('status')

        if status_param:
            queryset = queryset.filter(status=status_param)
        
        return queryset
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["status"] = self.request.GET.get('status')

        return context

