from django.urls import path

from .views import (PictureCreateView, PictureDeleteView, PictureDetailView,
                    PictureList, PictureUploadView, PictureUpdateView,CheckValidationView)

app_name = 'pictures'

urlpatterns = [
    path('', PictureCreateView.as_view(), name='top'),
    path('upload/', PictureUploadView.as_view(), name='picture_upload'),
    path('list/', PictureList.as_view(), name='picture_list'),
    path('delete/<int:pk>/', PictureDeleteView.as_view(), name='picture_delete'),
    path('detail/<int:pk>/', PictureDetailView.as_view(), name='picture_detail'),
    path('edit/<int:pk>/', PictureUpdateView.as_view(), name='picture_edit'),
    path('check_clean/', CheckValidationView.as_view(), name='picture_clean'),
]