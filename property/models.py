from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
import os
# Create your models here.
# print(settings.AUTH_USER_MODEL)
# User = settings.AUTH_USER_MODEL
# User = get_user_model()
class Property(models.Model):
    # user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    block = models.CharField(max_length=120)
    plot_num = models.CharField(max_length=120)
    area = models.CharField(max_length=50)
    is_alloted = models.BooleanField(default=False)
    files = models.FileField(upload_to=settings.MEDIA_ROOT,null=True,blank=True)
    
    @property
    def get_file_name(self):
        if self.files is not None:
            return os.path.basename(self.files.name)
    def __str__(self):
        return f'{self.block} - {self.area} - {self.plot_num}'
    
    class Meta:
        verbose_name_plural= 'properties'


class PropertyUser(models.Model):
    property = models.ForeignKey(Property,related_name='property_users', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=60)
    phone = models.CharField(max_length=12)

    def __str__(self):
        return f'{self.full_name}'