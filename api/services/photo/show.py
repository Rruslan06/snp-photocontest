from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from functools import lru_cache
from rest_framework import status

from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound
from service_objects.fields import ModelField

from models_app.models import Photo, User, Vote


class PhotoShowService(ServiceWithResult):
    """Сервис для вывода одной фотографии по ID"""
    photo_id = forms.IntegerField()
    user = ModelField(User, required=False)

    custom_validations = ['_validate_photo_exists']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._prepared_photo()
        return self

    @property
    @lru_cache
    def _photo(self):
        try:
            return (
                Photo.objects.select_related('author')
                .annotate(likes_count=Count('votes', distinct=True))
                .get(id=self.cleaned_data['photo_id'])
            )
        except ObjectDoesNotExist:
            return None

    def _prepared_photo(self):
        photo = self._photo
        user = self.cleaned_data.get('user')
        photo.has_voted = (
            Vote.objects.filter(photo=photo, author=user).exists()
            if user else False
        )
        return photo

    def _validate_photo_exists(self):
        if not self._photo:
            self.add_error(
                "photo_id",
                NotFound(message=f"Фотография с id {self.cleaned_data['photo_id']} не найдена.")
            )
            self.response_status = status.HTTP_404_NOT_FOUND