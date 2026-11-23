from celery import shared_task
from models_app.models import Photo
from models_app.models.photo import Photo_Status

@shared_task
def hard_delete_photo_task(photo_id):
    """
    Отложенная задача. Проверяет статус: если всё еще DEL, то удаляет навсегда.
    """
    try:
        photo = Photo.objects.get(id=photo_id)
        
        if photo.status == Photo_Status.ON_DELETION:
            photo.delete()
    except Photo.DoesNotExist:
        pass