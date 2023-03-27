from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Item, User, Tag

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields= '__all__'
        exclude =['seller', 'tags']


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields =['email', 'name']