from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from root import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('apps.user.urls')),
                  path('e-english/', include('apps.e_english.urls')),
                  path('admin2/', include('apps.admin2.urls')),
                  path('user/', include('apps.user.urls')),
              ] + debug_toolbar_urls()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

