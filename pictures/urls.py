from django.urls import path
from .views import PictureCreateView,PictureList

app_name = 'pictures'

urlpatterns = [
    # path('',IndexView.as_view(),name='index'),
    path('',PictureCreateView.as_view(),name='index'),
    path('list/',PictureList.as_view(),name='list'),
]

