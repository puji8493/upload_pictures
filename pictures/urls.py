from django.urls import path

from .views import PictureCreateView,PictureList,UpdateView,PictureDeleteView

app_name = 'pictures'

urlpatterns = [
    path('',PictureCreateView.as_view(),name='index'),
    path('upload/', UpdateView.as_view(), name='update'),
    path('list/',PictureList.as_view(),name='list'),
    path('delete/<int:pk>/',PictureDeleteView.as_view(),name='delete'),
]

