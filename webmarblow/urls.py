from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'Webmarblow Admin'
admin.site.site_title = 'Webmarblow'
admin.site.index_title = 'Manage website content'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
