
from os import name
from django.contrib import admin
from django.urls import path

from .views import *


urlpatterns = [
    path('', all_properties, name='list-properties'),
    path('add', add_property, name='add'),
    path('ajax-forms/', ajax_create_form),
    path('<int:id>/edit', property_update_view, name='edit-property'),
    path('search', property_search_view),
    path('<int:id>', property_detail_view),
    path('<int:id>/delete', property_delete_view, name='delete-record'),
    # path('<int:id>/delete', delete_user_view, name='delete-user'),
] 


