from django.urls import path
from .views import PictureCreateView,PictureList,PictureRegisterMessage,UpdateView,PictureDeleteView

app_name = 'pictures'

urlpatterns = [
    # path('',IndexView.as_view(),name='index'),
    path('',PictureCreateView.as_view(),name='index'),
    path('upload/', UpdateView.as_view(), name='update'),
    path('list/',PictureList.as_view(),name='list'),
    path('delete/<int:pk>/',PictureDeleteView.as_view(),name='delete'),
    path('register/',PictureRegisterMessage.as_view(),name='register')
]

