from django.db import models
from django.conf import settings
# Create your models here.


class Photo_Status(models.TextChoices):
    ON_MODERATION = 'MOD', "На проверке"
    APPROVED = "APR", "Одобрено"
    REJECTED = "REG", "Отклонено"


class Photo(models.Model):

    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to="photos/", verbose_name="Фотография")

    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photos', verbose_name="Автор")

    status = models.CharField(max_length=3, choices=Photo_Status.choices, default=Photo_Status.ON_MODERATION, verbose_name="Статус модерации")

    def __str__(self):
        return f"Название:{self.name}; Автор:{self.author.username}"



class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментария")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', verbose_name="Автор")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments', verbose_name="Фотография")

    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, verbose_name="Родитель")

    def __str__(self):
        return f"Комментарий от:{self.author.username} к Фото:{self.photo.name}" #Хрен знает что лучше пока выводить


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

    def __str__(self):
        return f"Лайк от:{self.author.username} к Фото:{self.photo.name}"

