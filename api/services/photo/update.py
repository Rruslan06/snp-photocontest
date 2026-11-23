from django import forms
from rest_framework import status
from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound
from service_objects.fields import ModelField
from models_app.models import Photo, User
from django.core.exceptions import ObjectDoesNotExist
from functools import lru_cache

# ИМПОРТЫ ДЛЯ HEIC
import io
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


class PhotoUpdateService(ServiceWithResult):
    photo_id = forms.IntegerField()
    name = forms.CharField(max_length=255, required=False)
    description = forms.CharField(required=False)
    photo = forms.ImageField(required=False) # Оставляем ImageField для безопасности
    user = ModelField(User)

    custom_validations = ['_validate_photo_exists', '_validate_photo_owner']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self._convert_heic() # <--- КОНВЕРТИРУЕМ ФАЙЛ (ЕСЛИ ОН ЕСТЬ)
            self.result = self._update_photo()
        return self

    @property
    @lru_cache
    def _photo(self):
        try:
            return Photo.objects.get(id=self.cleaned_data['photo_id'])
        except ObjectDoesNotExist:
            return None

    def _validate_photo_exists(self):
        if not self._photo:
            self.add_error("photo_id", NotFound(message="Фотография не найдена."))
            self.response_status = status.HTTP_404_NOT_FOUND

    def _validate_photo_owner(self):
        if not self._photo:
            return
        if self._photo.author != self.cleaned_data['user']:
            self.add_error("user", NotFound(message="Вы не можете изменить чужую фотографию."))
            self.response_status = status.HTTP_403_FORBIDDEN

    def _convert_heic(self):
        """Конвертируем HEIC в JPEG, если юзер загрузил новую фотку"""
        photo_file = self.cleaned_data.get('photo')
        

        if not photo_file:
            return


        file_name = photo_file.name.lower()
        if file_name.endswith('.heic') or file_name.endswith('.heif'):
            import pillow_heif
            
            # Читаем HEIC
            heif_file = pillow_heif.read_heif(photo_file)
            image = Image.frombytes(
                heif_file.mode, 
                heif_file.size, 
                heif_file.data, 
                "raw",
            )
            
            
            output_io = io.BytesIO()
            image.save(output_io, format='JPEG', quality=90)
            output_io.seek(0)
            
            # Создаем новый файл для Django
            new_file_name = file_name.rsplit('.', 1)[0] + '.jpg'
            new_photo = InMemoryUploadedFile(
                output_io, 'ImageField', new_file_name, 
                'image/jpeg', output_io.getbuffer().nbytes, None
            )
            
            # Заменяем HEIC на JPEG в очищенных данных
            self.cleaned_data['photo'] = new_photo

    def _update_photo(self):
        photo_obj = self._photo
        
        if self.cleaned_data.get('name'):
            photo_obj.name = self.cleaned_data['name']

        if self.cleaned_data.get('description'):
            photo_obj.description = self.cleaned_data['description']
            
        if self.cleaned_data.get('photo'):
            photo_obj.archive_photo = photo_obj.photo 
            photo_obj.photo = self.cleaned_data['photo'] 
            
        photo_obj.return_to_moderation()
        photo_obj.save() 
        return photo_obj