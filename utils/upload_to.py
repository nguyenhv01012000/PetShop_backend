import os
from django.utils.deconstruct import deconstructible


# Ref: https://stackoverflow.com/questions/25767787/django-cannot-create-migrations-for-imagefield-with-dynamic-upload-to-value
@deconstructible
class UploadTo:
    def __init__(self, model, field):
        self.model = model
        self.field = field
    
    def __eq__(self, other):
        return self.model == other.model and self.field == other.field
    
    def __call__(self, instance, filename):
        return os.path.join(
            self.model,
            str(instance.pk),
            self.field,
            filename
        )