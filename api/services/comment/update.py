from django import forms
from rest_framework import status
from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound
from service_objects.fields import ModelField
from models_app.models import Comment, User
from django.core.exceptions import ObjectDoesNotExist
from functools import lru_cache




class CommentUpdateService(ServiceWithResult):
    comment_id = forms.IntegerField()
    text = forms.CharField()
    user = ModelField(User)



    custom_validations = ['_validate_comment_exists', '_validate_comment_owner']



    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self._comment.text = self.cleaned_data['text']
            self._comment.save()
            self.result = self._comment
        return self



    @property
    @lru_cache
    def _comment(self):
        try:
            return Comment.objects.get(id=self.cleaned_data['comment_id'])
        except ObjectDoesNotExist:
            return None



    def _validate_comment_exists(self):
        if not self._comment:
            self.add_error("comment_id", NotFound(message="Комментарий не найден."))
            self.response_status = status.HTTP_404_NOT_FOUND



    def _validate_comment_owner(self):
        if not self._comment:
            return
        if self._comment.author != self.cleaned_data['user']:
            self.add_error("user", NotFound(message="Нельзя изменить чужой комментарий."))
            self.response_status = status.HTTP_403_FORBIDDEN