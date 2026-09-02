from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from motorartigos.views import update_server

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('motorartigos.urls')),
    path('update_server/', update_server, name='update_server'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
