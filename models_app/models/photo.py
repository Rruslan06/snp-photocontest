from django.db import models
from django.conf import settings
from models_app.utils.upload import *
from django.db.models.signals import pre_save, post_save, post_delete

from django_fsm import FSMField, transition

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

    status = FSMField(max_length=20, choices=Photo_Status.choices, default=Photo_Status.ON_MODERATION, verbose_name="Статус модерации")

    pending_photo = models.ImageField(upload_to=uploaded_file_path, verbose_name="Новая версия (на модерации)", blank=True, null=True)

    def __str__(self):
        return f"Название:{self.name}; Автор:{self.author.username}"
    
    class Meta:
        app_label = "models_app"
        db_table = "Photo"

    @transition(field=status, source=Photo_Status.ON_MODERATION, target=Photo_Status.APPROVED)
    def approve(self):
        # Здесь можно написать отправление пуш-уведомления на будущее
        if self.pending_photo:
            self.photo = self.pending_photo
            self.pending_photo = None


    # Правило: Отклонить можно ТОЛЬКО из статуса ON_MODERATION
    @transition(field=status, source=Photo_Status.ON_MODERATION, target=Photo_Status.REJECTED)
    def reject(self):
        pass

    


pre_save.connect(skip_saving_file, sender=Photo)
post_save.connect(save_file, sender=Photo)
post_delete.connect(file_delete, sender=Photo)