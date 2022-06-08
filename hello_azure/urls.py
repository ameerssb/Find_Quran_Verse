from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hello', views.hello, name='hello'),
    path('recorder', views.recorder, name="recorder"),
    path('translator', views.translator, name="translator")
]