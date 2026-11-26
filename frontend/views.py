from django.shortcuts import render

from django.views.generic import TemplateView

from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.mixins import LoginRequiredMixin


class FrontendRegisterView(TemplateView):
    template_name = 'frontend/register.html'

class FrontendIndexView(TemplateView):
    template_name = 'frontend/index.html'


class FrontendDetailView(TemplateView):
    template_name = 'frontend/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Прокидываем ID из URL в шаблон (чтобы JS мог его подхватить)
        context['photo_id'] = self.kwargs.get('pk') 
        return context
    

class FrontendLoginView(TemplateView):
    template_name = 'frontend/login.html'


class FrontendProfileView(TemplateView):
    template_name = 'frontend/profile.html'

class FrontendUploadView(TemplateView):
    template_name = 'frontend/upload.html'


class FrontendSocialCallbackView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/social_callback.html'
    login_url = '/login/' #Чтоб перекидывало если новый чел

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        refresh = RefreshToken.for_user(user)

       
        social_account = user.socialaccount_set.filter(provider='yandex').first()
        avatar_url = ""
        if social_account:
            extra = social_account.extra_data
            avatar_id = extra.get("default_avatar_id")
            if avatar_id and not extra.get("is_avatar_empty", False):
                avatar_url = f"https://avatars.yandex.net/get-yapic/{avatar_id}/islands-200"

        display_name = user.get_full_name() or user.first_name or user.username

        context['access_token'] = str(refresh.access_token)
        context['refresh_token'] = str(refresh)
        context['username'] = user.username
        context['display_name'] = display_name
        context['email'] = user.email or ''
        context['avatar_url'] = avatar_url
        return context
