import re  #

from django.core.files import File
from django.db.models.fields.files import FieldFile

def uploaded_file_path(instance, filename, **kwargs):
    path = re.sub(r"(\d.+)(\d{3})(\d{3})$", r"\1/\2/\3", f"{instance.id:09d}")
    return f"{instance.__class__.__name__.lower()}s/{path}/{kwargs.get('field_name', 'file')}/{filename}"


def skip_saving_file(sender, instance, **kwargs):
    if not instance.pk and not sender.__name__ == "Migration":
        file_fields = [
            field
            for field in instance.__dict__.keys()
            # if issubclass(instance.__dict__[field].__class__, FieldFile)
            # or issubclass(instance.__dict__[field].__class__, UploadedFile)
            # or
            if issubclass(instance.__dict__[field].__class__, File)
        ]
        for field in file_fields:
            setattr(instance, f"tmp_{field}_field", getattr(instance, field))
            setattr(instance, field, None)


def save_file(sender, instance, created, **kwargs):
    if created and not sender.__name__ == "Migration":
        file_fields = [
            field
            for field in instance.__dict__.keys()
            if issubclass(instance.__dict__[field].__class__, FieldFile)
            and not instance.__dict__[field]
        ]
        for field in file_fields:
            if hasattr(instance, f"tmp_{field}_field"):
                setattr(instance, field, getattr(instance, f"tmp_{field}_field"))
        instance.save()


def file_delete(sender, instance, **kwargs):
    instance.file.delete(False)