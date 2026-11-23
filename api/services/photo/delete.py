from django import forms
from rest_framework import status
from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound
from service_objects.fields import ModelField
from django.core.exceptions import ObjectDoesNotExist
from functools import lru_cache
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from models_app.models import Photo, User
from api.tasks import hard_delete_photo_task


class PhotoDeleteService(ServiceWithResult):
    photo_id = forms.IntegerField()
    user = ModelField(User)

    custom_validations = ['_validate_photo_exists', '_validate_photo_owner']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self._photo.send_on_deletion()
            self._photo.save()


            #Уведы для тех, комменты которого пропадут с уделаением фотки
            self._notify_commenters()


            hard_delete_photo_task.apply_async(args=[self._photo.id], countdown=120)

            self.result = {"message": "Фотография скрыта и будет окончательно удалена через 2 минуты."}
        return self


    def _notify_commenters(self):
        commenters = User.objects.filter(comments__photo=self._photo).exclude(id=self._user.id).distinct()
        
        if commenters.exists():
            channel_layer = get_channel_layer()
            message = (
                f"Фотография '{self._photo.name}', к которой вы оставили комментарий, "
                f"отправлена на удаление. Ваш комментарий скоро будет удален."
            )
            for commenter in commenters:
                async_to_sync(channel_layer.group_send)(
                    f"user_{commenter.id}",
                    {"type": "send_notification", "message": message}
                )



    @property
    @lru_cache
    def _photo(self):
        try:
            return Photo.objects.get(id=self.cleaned_data['photo_id'])
        except ObjectDoesNotExist:
            return None



    @property
    def _user(self):
        return self.cleaned_data['user']



    def _validate_photo_exists(self):
        if not self._photo:
            self.add_error("photo_id", NotFound(message="Фотография не найдена."))
            self.response_status = status.HTTP_404_NOT_FOUND



    def _validate_photo_owner(self):
        if not self._photo:
            return
        if self._photo.author != self._user:
            self.add_error("user", NotFound(message="Вы не можете удалить чужую фотографию."))
            self.response_status = status.HTTP_403_FORBIDDEN