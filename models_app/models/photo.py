from django.db import models
from django.conf import settings
from models_app.utils.upload import *
from django.db.models.signals import pre_save, post_save, post_delete

from django_fsm import FSMField, transition, RETURN_VALUE

# Create your models here.

class Photo_Status(models.TextChoices):
    ON_MODERATION = 'MOD', "На проверке"
    APPROVED = "APR", "Одобрено"
    REJECTED = "REG", "Отклонено"
    ON_DELETION = "DEL", "На удалении"


def get_previous_status(instance):
    print(f"DEBUG: Пытаемся вернуть статус: {instance.previous_status}")
    return instance.previous_status or Photo_Status.ON_MODERATION

class Photo(models.Model):

    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to=uploaded_file_path, verbose_name="Фотография")

    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photos', verbose_name="Автор")

    status = FSMField(max_length=50, choices=Photo_Status.choices, default=Photo_Status.ON_MODERATION, verbose_name="Статус модерации")

    
    previous_status = models.CharField(max_length=50, blank=True, null=True)

    archive_photo = models.ImageField(upload_to=uploaded_file_path, verbose_name="Старая фотка(Архив)", blank=True, null=True)


    def __str__(self):
        return f"Название:{self.name}; Автор:{self.author.username}"
    
    class Meta:
        app_label = "models_app"
        db_table = "Photo"


    @transition(field=status, source=Photo_Status.ON_MODERATION, target=Photo_Status.APPROVED)
    def approve(self):
        # Здесь можно написать отправление пуш-уведомления на будущее
        pass


    # Правило: Отклонить можно ТОЛЬКО из статуса ON_MODERATION
    @transition(field=status, source=Photo_Status.ON_MODERATION, target=Photo_Status.REJECTED)
    def reject(self):
        pass

    
    @transition(field=status, source="*", target=Photo_Status.ON_MODERATION)
    def return_to_moderation(self):
        pass

    @transition(field=status, source="*", target=Photo_Status.ON_DELETION)
    def send_on_deletion(self):
        """Мягкое удаление"""
        print(f"DEBUG: Пытаюсь сохранить статус: {self.status}, тип: {type(self.status)}")
        self.previous_status = self.status.value if hasattr(self.status, 'value') else self.status
        print(f"DEBUG: Сохраняю статус: {self.previous_status}")



    @transition(field=status, source=Photo_Status.ON_DELETION, target=RETURN_VALUE(Photo_Status.APPROVED, Photo_Status.ON_MODERATION, Photo_Status.REJECTED))     
    def restore(self):
        # Возвращаем строковое значение, а FSM сама переведет в этот статус
        return self.previous_status or Photo_Status.ON_MODERATION


pre_save.connect(skip_saving_file, sender=Photo)
post_save.connect(save_file, sender=Photo)
post_delete.connect(file_delete, sender=Photo)