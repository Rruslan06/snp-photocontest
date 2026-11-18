from django import forms
from service_objects.services import ServiceWithResult
from models_app.models import Photo, Vote, User
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from service_objects.errors import NotFound
from rest_framework import status
from service_objects.fields import ModelField

from functools import lru_cache


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class ToggleVoteService(ServiceWithResult):
    
    photo_id = forms.IntegerField()
    # user_id = forms.IntegerField() 
    user  = ModelField(User)

    custom_validations = ["_validate_photo_exist"]
    
    def process(self):
        
        self.run_custom_validations()
        if self.is_valid():
            self._vote()
        return self
    

    def _vote(self):

        vote = Vote.objects.filter(photo=self._photo, author=self._user).first()
        
        if vote:
            vote.delete()
            liked = False
        else:
            Vote.objects.create(photo=self._photo, author=self._user)
            liked = True

        self.result = {"liked": liked, "likes_count": self._photo.votes.count()}


        # Уведомление автору фото (если лайкает не он сам)
        if self._user.id != self._photo.author.id:
            action = "лайкнул" if liked else "снял лайк с"
            message = f"Пользователь {self._user.username} {action} вашего фото '{self._photo.name}'. Текущее количество голосов: {self._photo.votes.count()}"
            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{self._photo.author.id}",
                {"type": "send_notification", "message": message}
            )
        
    
    @property
    @lru_cache
    def _photo(self):
        try:
            return Photo.objects.get(id=self.cleaned_data["photo_id"])
        except ObjectDoesNotExist:
            return None
        
    @property
    def _user(self):
        return self.cleaned_data["user"]

    def _validate_photo_exist(self):
        if not self._photo:
            self.add_error(
                "photo_id",
                NotFound(
                    message=f"Photo with id = {self.cleaned_data["photo_id"]} not found",
                ),
            )
            self.response_status = status.HTTP_404_NOT_FOUND



