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




class PhotoListView(generic.ListView):
    model = Photo
    template_name = 'site_app/index.html'
    context_object_name = 'photos'
    paginate_by = 4

    #Потом переопределить чтобы отображались только прошедшие модерацию
    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get('q', '')
        if q:
            search_query = Q(name__icontains=q) | Q(author__username__icontains=q) | Q(description__icontains=q)
            queryset = queryset.filter(search_query)

        sort_param = self.request.GET.get('sort', 'date_desc')

        if sort_param == 'date_asc':
            return queryset.order_by('date')  # Сначала старые
        else:
            return queryset.order_by('-date') # Сначала новые
        

    def get_context_data(self, **kwargs):
        # Получаем стандартный контекст (в нем уже есть объект из ОсновнойМодели как 'object')
        context = super().get_context_data(**kwargs)    

        context['sort_param'] = self.request.GET.get('sort', 'date_desc')
        context['search_query'] = self.request.GET.get('q', '')

        return context




class PhotoDetailView(generic.DetailView):
    model = Photo #оснновная модель 
    template_name = 'site_app/detail.html'
    context_object_name = 'photo'

    def get_context_data(self, **kwargs):
        # Получаем стандартный контекст (в нем уже есть объект из ОсновнойМодели как 'object')
        context = super().get_context_data(**kwargs)

        # По умолчанию считаем, что лайка нет
        context['has_voted'] = False 
        if self.request.user.is_authenticated:
            # Если в базе есть хоть один лайк от этого юзера к этому фото, вернет True
            context['has_voted'] = Vote.objects.filter(photo=self.object, author=self.request.user).exists()
    
        context['comments'] = Comment.objects.filter(photo=self.object).filter(parent=None).order_by('-date')

        return context
    


@login_required
def add_comment(request, pk):
    if request.method == "POST":
        photo = get_object_or_404(Photo, pk=pk)
        
        text = request.POST.get('text')
        
        parent_id =  request.POST.get('parent_id')

        if text:
            if parent_id:
                father = get_object_or_404(Comment, id=parent_id)
                if father.parent_id:
                    final_parent = father.parent
                else:
                    final_parent = father
                Comment.objects.create(text=text, author=request.user, photo=photo, parent=final_parent)

            else:    
                Comment.objects.create(text=text, author=request.user, photo=photo)
    return redirect("site_app:detail_page", pk=pk)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        if request.user == comment.author:
            if not comment.replies.exists():
                comment.delete()
    return redirect("site_app:detail_page", pk=comment.photo.pk)


@login_required
def toggle_vote(request, pk):
    if request.method == "POST":
        photo = get_object_or_404(Photo, pk=pk)
        vote = Vote.objects.filter(photo=photo, author=request.user).first()
        if vote:
            vote.delete()
        else:
            Vote.objects.create(photo=photo, author=request.user)
    return redirect("site_app:detail_page", pk=pk)



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

        


class PhotoCreateView(LoginRequiredMixin, generic.CreateView):
    model = Photo
    template_name = 'site_app/upload.html'
    fields = ['name', 'description', 'photo']


    #Куда перенаправлять если форма заполнена корректно
    def get_success_url(self):
        return reverse('site_app:profile') 

    #
    def form_valid(self, form):

        #Чтобы автор сразу пробрасывался
        form.instance.author = self.request.user
        
        return super().form_valid(form)