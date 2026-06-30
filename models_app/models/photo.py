from django.db import models
from django.conf import settings
from models_app.utils.upload import *
from django.db.models.signals import pre_save, post_save, post_delete
# Create your models here.

class Photo_Status(models.TextChoices):
    ON_MODERATION = 'MOD', "На проверке"
    APPROVED = "APR", "Одобрено"
    REJECTED = "REG", "Отклонено"


class Photo(models.Model):

    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to=uploaded_file_path, verbose_name="Фотография")

    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photos', verbose_name="Автор")

    status = models.CharField(max_length=3, choices=Photo_Status.choices, default=Photo_Status.ON_MODERATION, verbose_name="Статус модерации")

    def __str__(self):
        return f"Название:{self.name}; Автор:{self.author.username}"
    
    class Meta:
        app_label = "models_app"
        db_table = "Photo"


pre_save.connect(skip_saving_file, sender=Photo)
post_save.connect(save_file, sender=Photo)
post_delete.connect(file_delete, sender=Photo)