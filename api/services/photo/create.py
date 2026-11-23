from django import forms
from django.core.paginator import EmptyPage, Page, Paginator
from django.db.models import Q, Count
from rest_framework import status

from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound
from models_app.models import Photo, User

from service_objects.fields import ModelField
from django.core.exceptions import ObjectDoesNotExist

from functools import lru_cache

from models_app.models.photo import Photo_Status

import rest_framework as settings
from django.db import models


import io
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile



class PhotoCreateService(ServiceWithResult):
    """Сервис для загрузки новой фотографии"""
    name = forms.CharField(max_length=255)
    description = forms.CharField()
    
    photo = forms.ImageField()
    author = ModelField(User) 

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self._convert_heic()
            self.result = self._create_photo()
        return self


    def _convert_heic(self):
        """Проверяет файл, и если это HEIC - делает из него JPEG"""
        photo_file = self.cleaned_data.get('photo')
        if not photo_file:
            return
            
        file_name = photo_file.name.lower()
        if file_name.endswith('.heic') or file_name.endswith('.heif'):
            import pillow_heif
            
            
            heif_file = pillow_heif.read_heif(photo_file)
            image = Image.frombytes(
                heif_file.mode, 
                heif_file.size, 
                heif_file.data, 
                "raw",
            )
            
            # Сохраняем в оперативную память как JPEG
            output_io = io.BytesIO()
            image.save(output_io, format='JPEG', quality=90)
            output_io.seek(0)
            
            # Формируем новый файл для Django
            new_file_name = file_name.rsplit('.', 1)[0] + '.jpg'
            new_photo = InMemoryUploadedFile(
                output_io, 'ImageField', new_file_name, 
                'image/jpeg', output_io.getbuffer().nbytes, None
            )
            
            # Заменяем оригинальный HEIC на новый JPEG в очищенных данных
            self.cleaned_data['photo'] = new_photo


    def _create_photo(self):
        
        return Photo.objects.create(
            name=self.cleaned_data['name'],
            description=self.cleaned_data['description'],
            photo=self.cleaned_data['photo'],
            author=self.cleaned_data['author']
        )