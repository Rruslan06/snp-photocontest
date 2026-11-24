from django.db import models


class MassNotification(models.Model):

    message = models.TextField(verbose_name="Текст сообщения")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")


    def __str__(self):
        return f"Рассылка от {self.created_at.strftime('%d.%m.%Y %H:%M') }: {self.message[:40]}"

    class Meta:
        app_label = "models_app"
        db_table = "MassNotification"
        verbose_name = "Массовое уведомление"
        verbose_name_plural = "Массовые уведомления"