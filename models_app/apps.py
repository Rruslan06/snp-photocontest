from django.apps import AppConfig

class ModelsappConfig(AppConfig):
    name = 'models_app'

    def ready(self):
        # Эта функция запускается 1 раз 
        
        try:
            import pillow_heif
            pillow_heif.register_heif_opener()
        except ImportError:
            pass