from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
#Временно переопределили модель пользователей и теперь это основная
    pass

    class Meta:
        app_label = "models_app"
        db_table = "User"