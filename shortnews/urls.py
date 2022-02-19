from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from shortnews import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('captcha/', include('captcha.urls')),
    path('wiki/', include('wiki.urls')),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)