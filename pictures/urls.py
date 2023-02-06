from django.urls import path

from .views import PictureCreateView,PictureList,PictureUploadView,PictureDeleteView


app_name = 'pictures'

urlpatterns = [
    path('',PictureCreateView.as_view(),name='top'),
    path('upload/', PictureUploadView.as_view(), name='picture_upload'),
    path('list/',PictureList.as_view(),name='picture_list'),
    path('delete/<int:pk>/',PictureDeleteView.as_view(),name='picture_delete'),
]

