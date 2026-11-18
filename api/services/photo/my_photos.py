from django import forms
from django.core.paginator import Paginator, EmptyPage, Page
from rest_framework import status
from django.conf import settings




from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound
from service_objects.fields import ModelField

from models_app.models import Photo, User
from models_app.models.photo import Photo_Status

class ProfilePhotoListService(ServiceWithResult):
    """Сервис для вывода фотографий текущего пользователя в личном кабинете"""
    
    
    status_filter = forms.ChoiceField(choices=Photo_Status.choices, required=False)
    page = forms.IntegerField(required=False, min_value=1)
    per_page = forms.IntegerField(initial=8, required=False, min_value=1, max_value=100)
    
    
    user = ModelField(User)

    def process(self):
        if self.is_valid():
            self.result = self._paginated_photos
        return self


    @property
    def _paginated_photos(self) -> Page:
        try:
            return Paginator(
                self._prepared_photos,
                self.cleaned_data.get("per_page") or settings.REST_FRAMEWORK["PAGE_SIZE"],
            ).page(self.cleaned_data.get("page") or 1)
        except EmptyPage:
            return Paginator(
                Photo.objects.none(),
                self.cleaned_data.get("per_page") or settings.REST_FRAMEWORK["PAGE_SIZE"],
            ).page(1)

    @property
    def _prepared_photos(self):
        
        queryset = Photo.objects.filter(author=self.cleaned_data['user']).order_by('-date')

        
        status_term = self.cleaned_data.get('status_filter')
        if status_term:
            queryset = queryset.filter(status=status_term)

        return queryset