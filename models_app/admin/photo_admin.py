from django.contrib import admin
from django.contrib import messages 
from django_fsm import TransitionNotAllowed 
from models_app.models.photo import Photo

from django.utils.html import format_html

@admin.action(description='Одобрить выбранные фотографии')
def approve_photos(modeladmin, request, queryset):
    success_count = 0
    error_count = 0
    
    for photo in queryset:
        try:
            photo.approve() 
            photo.save()
            success_count += 1
        except TransitionNotAllowed:
            
            error_count += 1

    # Выводим красивые сообщения модератору
    if success_count > 0:
        modeladmin.message_user(request, f'Успешно одобрено: {success_count} фото.', messages.SUCCESS)
    if error_count > 0:
        modeladmin.message_user(request, f'Ошибка: {error_count} фото уже имеют другой статус!', messages.ERROR)


@admin.action(description='Отклонить выбранные фотографии')
def reject_photos(modeladmin, request, queryset):
    success_count = 0
    error_count = 0
    
    for photo in queryset:
        try:
            photo.reject()
            photo.save()
            success_count += 1
        except TransitionNotAllowed:
            error_count += 1

    if success_count > 0:
        modeladmin.message_user(request, f'Успешно отклонено: {success_count} фото.', messages.SUCCESS)
    if error_count > 0:
        modeladmin.message_user(request, f'Ошибка: {error_count} фото нельзя отклонить!', messages.ERROR)




@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):

    def image_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 50px; border-radius: 5px;" />', obj.photo.url)
        return "Нет фото"
    
    image_preview.short_description = 'Основная(Новая) фотография'


    def archive_image_preview(self, obj):
        if obj.archive_photo:
            return format_html('<img src="{}" style="max-height: 50px; border-radius: 5px;" />', obj.archive_photo.url)
        return "Нет фото"

    archive_image_preview.short_description = "Старая фотография"

    list_display = ('image_preview', 'archive_image_preview','name', 'author', 'status', 'date')
    list_filter = ('status', 'date')
    search_fields = ('name', 'description', 'author__username')
    readonly_fields = ('date','archive_photo')
    
    # Регистрируем наши кнопки в админке!
    actions = [approve_photos, reject_photos]