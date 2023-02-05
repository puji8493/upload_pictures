from django.urls import path
from .views import PictureCreateView,PictureList,PictureRegisterMessage

app_name = 'pictures'

urlpatterns = [
    # path('',IndexView.as_view(),name='index'),
    path('',PictureCreateView.as_view(),name='index'),
    path('list/',PictureList.as_view(),name='list'),
    path('register/',PictureRegisterMessage.as_view(),name='register')
]

