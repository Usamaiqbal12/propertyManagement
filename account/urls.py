from django.urls import path
from .views import *

urlpatterns = [
    path('login/', property_login, name='login'),
    path('logout/', property_logout, name="logout"),
    path('register/', property_register, name="register"),
    path('activate/<uidb64>/<token>', activate, name='activate')
] 

#Updated
#another update


