from django.db import models
from django.conf import settings
from models_app.models.photo import Photo
# Create your models here.

class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментария")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', verbose_name="Автор")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments', verbose_name="Фотография")

    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, verbose_name="Родитель", related_name='replies')

    def __str__(self):
        return f"Комментарий от:{self.author.username} к Фото:{self.photo.name}" #Хрен знает что лучше пока выводить

    class Meta:
        db_table = "Comment"
        app_label = "models_app"