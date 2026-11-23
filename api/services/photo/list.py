from django import forms
from django.core.paginator import EmptyPage, Page, Paginator
from django.db.models import Q, Count
from rest_framework import status

from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound
from models_app.models import Photo, User

from service_objects.fields import ModelField
from django.core.exceptions import ObjectDoesNotExist

from functools import lru_cache

from models_app.models.photo import Photo_Status

from django.conf import settings
from django.db import models

class SortDirection(models.TextChoices):
    ASC = 'asc', "По возрастанию"
    DESC = "desc", "По убыванию"

class SortField(models.TextChoices):
    DATE = 'date', 'По дате'
    VOTE = 'likes_count', 'По лайкам'
    COMMENT = 'comment_count', 'По комментариям'

class PhotoListService(ServiceWithResult):
    search_query = forms.CharField(max_length=30, required=False, min_length=3)
    sort_field = forms.ChoiceField(choices=SortField.choices, required=False, initial=SortField.DATE.value) 
    sort_direction = forms.ChoiceField(choices=SortDirection.choices, required=False, initial=SortDirection.DESC.value)
    page = forms.IntegerField(required=False, min_value=1)
    per_page = forms.IntegerField(initial=8, required=False, min_value=1, max_value=100)


    def process(self):

        if self.is_valid():
            self.result = self._paginated_photos
        return self


    @property
    def _paginated_photos(self) -> Page:
        try:
            return Paginator(
                self._prepared_photos,
                self.cleaned_data.get("per_page")
                or settings.REST_FRAMEWORK["PAGE_SIZE"],
            ).page(self.cleaned_data.get("page") or 1)
        except EmptyPage:
            return Paginator(
                Photo.objects.none(),
                self.cleaned_data.get("per_page")
                or settings.REST_FRAMEWORK["PAGE_SIZE"],
            ).page(1)


    @property
    def _prepared_photos(self):
        
        queryset = Photo.objects.filter(status=Photo_Status.APPROVED).select_related('author')


        search_term = self.cleaned_data.get("search_query")
        if search_term:
            filter_for_photo = Q(name__icontains=search_term) | Q(author__username__icontains=search_term) | Q(description__icontains=search_term)
            queryset = queryset.filter(filter_for_photo)

        sort_direction = self.cleaned_data.get("sort_direction") or "desc"
        sort_term = self.cleaned_data.get("sort_field") or "date"
        queryset = queryset.annotate(
            likes_count=Count('votes', distinct=True), 
            comment_count=Count('comments', distinct=True)
        )

        queryset=queryset.order_by(("-" if sort_direction=="desc" else "") + sort_term)
        
        return queryset

