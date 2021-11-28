
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings as django_settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('property/', include('property.urls')),
    path('', include('account.urls')),
    path('', include('dashboard.urls')),
] + static(django_settings.MEDIA_URL, document_root=django_settings.MEDIA_ROOT)


