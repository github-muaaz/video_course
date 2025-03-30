from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


def redirect_to_videos(request):
    return redirect("videos")


urlpatterns = [
    path('', redirect_to_videos, name='home'),
    path('admin/', admin.site.urls),
    path('videos/', include('videos.urls')),
    path("accounts/", include("django.contrib.auth.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
