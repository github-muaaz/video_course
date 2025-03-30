from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index, subscribe, unsubscribe, protected_media


urlpatterns = [
    path('', index, name='videos'),
    path("subscribe/", subscribe, name="subscribe"),
    path("unsubscribe/", unsubscribe, name="unsubscribe"),
    path("media/protected/<path:file_path>", protected_media, name="protected_media"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
