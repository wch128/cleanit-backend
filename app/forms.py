from django.forms import ModelForm
from .models import OrgPhoto, AlertPhoto

class OrgPhotoForm(ModelForm):
    class Meta:
        model = OrgPhoto
        fields = ('image', 'caption')

class AlertPhotoForm(ModelForm):
    class Meta:
        model = AlertPhoto
        fields = ('image', 'caption')