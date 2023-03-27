from django.contrib import admin
from .models import User, Tag, Item, Cart


# Register your models here.
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Item)
admin.site.register(Cart)