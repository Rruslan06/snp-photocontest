from django.contrib import admin
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from models_app.models import User, MassNotification


@admin.register(MassNotification)
class MassNotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_at')
    readonly_fields = ("created_at",)

    def save_model(self, request, obj, form, change):

        super().save_model(request, obj, form, change)
    
        if not change:
            channel_layer = get_channel_layer()
            users = User.objects.all()
            for user in users:
                async_to_sync(channel_layer.group_send)(
                    f"user_{user.id}",
                    {"type": "send_notification", "message": obj.message}
                )
            self.message_user(
                request,
                "Массовое уведомление успешно отправлено всем онлайн-пользователям!",
                messages.SUCCESS
            )