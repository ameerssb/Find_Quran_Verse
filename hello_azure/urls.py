from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hello', views.hello, name='hello'),
    path('translator', views.translator, name="translator"),
    path('androidAudio', views.AndroidAudio, name="AndroidAudio"),
    path('androidText', views.AndroidText, name="androidText")
]

#if settings.DEBUG:
#   urlpatterns = static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)