from django import forms
from service_objects.services import ServiceWithResult
from models_app.models import Photo, Vote
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from service_objects.errors import NotFound
from rest_framework import status
from service_objects.fields import ModelField

from functools import lru_cache


class ToggleVoteService(ServiceWithResult):
    
    photo_id = forms.IntegerField()
    # user_id = forms.IntegerField() 
    user  = ModelField()

    custom_validations = ["_validate_photo_exist"]
    
    def process(self):
        
        self.run_custom_validations()
        if self.is_valid():
            self._vote()
        return self
    

    def _vote(self):

        vote = Vote.objects.filter(photo=self._photo, author_id=self._user).first()
        
        if vote:
            vote.delete()
        else:
            Vote.objects.create(photo=self._photo, author_id=self._user)

    
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