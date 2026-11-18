from django.shortcuts import render

from django.views.generic import TemplateView



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

