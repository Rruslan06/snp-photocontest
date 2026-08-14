from django.shortcuts import render, get_object_or_404, redirect #Нужен чтобы использовать шаблоны(короткий путь) и ошибку 404

from django.urls import reverse #Как в шаблонах в Питоне используем удобную запись и не хардкордим страницу куда перейти

from django.views import generic, View #Чтобы использовать базовые представления(Generic View) 

from django.db.models import F #Чтобы работать с полями и не было состояния гонки

from django.http import HttpResponse, HttpResponseRedirect #Чтобы перенаправлять пользователя с POST на GET запросы(страницы)

from models_app.models import Photo, Comment, Vote

from django.db.models import Q # Q-объекты для гибких условий фильтрации

from django.contrib.auth.mixins import LoginRequiredMixin #Миксин для проверки что пользователь авторизован

from django.contrib.auth.decorators import login_required #Декоратор чтобы функиця проверяла что пользователь авторизован
# Create your views here.


# @login_required
# def toggle_vote(request, pk):
#     if request.method == "POST":
#         photo = get_object_or_404(Photo, pk=pk)
#         vote = Vote.objects.filter(photo=photo, author=request.user).first()
#         if vote:
#             vote.delete()
#         else:
#             Vote.objects.create(photo=photo, author=request.user)
#     return redirect("site_app:detail_page", pk=pk)

class ToggleVoteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args,**kwargs):
        
        photo = get_object_or_404(Photo, pk=pk)
        vote = Vote.objects.filter(photo=photo, author=request.user).first()
        
        if vote:
            vote.delete()
        else:
            Vote.objects.create(photo=photo, author=request.user)
            
        return redirect("site_app:detail_page", pk=pk)