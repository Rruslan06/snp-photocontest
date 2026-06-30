from django.db import models
from django.conf import settings
from models_app.models.photo import Photo
# Create your models here.



class Vote(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes', verbose_name="Автор")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='votes', verbose_name="Фото")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата лайка")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'photo'],
                name="unique_vote_for_photo"
            )
        ]
        app_label = "models_app"
        db_table = "Vote"

    def __str__(self):
        return f"Лайк от:{self.author.username} к Фото:{self.photo.name}"

