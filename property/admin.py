from django.contrib import admin

from property.models import Property, PropertyUser

# Register your models here.

admin.site.register(Property)
admin.site.register(PropertyUser)