from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('audiotranslator/', views.AudioTranslator.as_view(), name='hello'),
    path('texttranslator/', views.TextTranslator.as_view(), name="translator"),
    path('androidAudio', views.AndroidAudio, name="AndroidAudio"),
    path('androidText', views.AndroidText, name="androidText"),
]