from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hello', views.hello, name='hello'),
    path('translator', views.translator, name="translator"),
    path('androidAudio', views.AndroidAudio, name="AndroidAudio"),
    path('androidText', views.AndroidText, name="androidText")
]