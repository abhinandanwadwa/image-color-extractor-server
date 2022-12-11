from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("api/getsinglecolor", views.getSingleColor, name="getSingleColor"),
]
# + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)