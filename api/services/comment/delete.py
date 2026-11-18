from django import forms
from rest_framework import status
from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound
from service_objects.fields import ModelField
from models_app.models import Comment, User
from django.core.exceptions import ObjectDoesNotExist
from functools import lru_cache

class CommentDeleteService(ServiceWithResult):
    comment_id = forms.IntegerField()
    user = ModelField(User)

    

    custom_validations = ['_validate_comment_exists', '_validate_comment_owner', '_validate_no_replies']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self._comment.delete()
            self.result = {"message": "Комментарий успешно удален"}
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
            return None
        if self._comment.author != self.cleaned_data['user']:
            self.add_error("user", NotFound(message="Нельзя удалить чужой комментарий."))
            self.response_status = status.HTTP_403_FORBIDDEN



    def _validate_no_replies(self):
        if not self._comment:
            return
        
        if self._comment.replies.exists():
            self.add_error("comment_id", NotFound(message="Нельзя удалить комментарий, на который уже ответили."))
            
            self.response_status = status.HTTP_400_BAD_REQUEST