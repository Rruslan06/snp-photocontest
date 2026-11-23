from django import forms
from rest_framework import status
from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound
from service_objects.fields import ModelField
from models_app.models import Photo, User
from django.core.exceptions import ObjectDoesNotExist
from functools import lru_cache
from models_app.models.photo import Photo_Status



class PhotoRestoreService(ServiceWithResult):
    photo_id = forms.IntegerField()
    user = ModelField(User)

    custom_validations = ['_validate_photo']

    def process(self):

        self.run_custom_validations()

        if self.is_valid():
            self._photo.restore() 
            self._photo.save()
            self.result = {"message": "Удаление отменено, фотография восстановлена."}
        return self

    @property
    @lru_cache
    def _photo(self):
        try:
            return Photo.objects.get(id=self.cleaned_data['photo_id'])
        except ObjectDoesNotExist:
            return None


    def _validate_photo(self):

        if not self._photo:

            self.add_error("photo_id", NotFound(message="Фотография не найдена."))
            self.response_status = status.HTTP_404_NOT_FOUND
            return  None
        
        if self._photo.author != self.cleaned_data['user']:
            self.add_error("user", NotFound(message="Это не ваша фотография."))
            self.response_status = status.HTTP_403_FORBIDDEN
            return None
        
        if self._photo.status != Photo_Status.ON_DELETION:
            self.add_error("photo_id", NotFound(message="Эта фотография не находится в процессе удаления."))
            self.response_status = status.HTTP_400_BAD_REQUEST