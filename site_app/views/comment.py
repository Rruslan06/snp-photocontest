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

class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, pk, *args,**kwargs):
        photo = get_object_or_404(Photo, pk=pk)
        
        text = request.POST.get('text')
        
        parent_id =  request.POST.get('parent_id')

        if text:
            if parent_id:
                father = get_object_or_404(Comment, id=parent_id)
                if father.parent_id and father.parent.parent_id:
                    final_parent = father.parent
                else:
                    final_parent = father
                Comment.objects.create(text=text, author=request.user, photo=photo, parent=final_parent)

            else:    
                Comment.objects.create(text=text, author=request.user, photo=photo)
        return redirect("site_app:detail_page", pk=pk)




class DeleteCommentView(LoginRequiredMixin, View):
    def post(self, request, pk, *args,**kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        if request.user == comment.author:
            if not comment.replies.exists():
                comment.delete()
        return redirect("site_app:detail_page", pk=comment.photo.pk)