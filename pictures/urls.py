from django.urls import path

from .views import (PictureCreateView, PictureDeleteView, PictureDetailView,
                    PictureList, PictureUploadView, PictureUpdateView,
                    CheckValidationView,CheckValidationViewByModelForm,
                    EditViewByForm,EditView,PictureDeleteByForm)

app_name = 'pictures'

urlpatterns = [
    path('', PictureCreateView.as_view(), name='top'),
    path('upload/', PictureUploadView.as_view(), name='picture_upload'),
    path('list/', PictureList.as_view(), name='picture_list'),
    path('delete/<int:pk>/', PictureDeleteView.as_view(), name='picture_delete'),
    path('delete_form/<int:pk>/', PictureDeleteByForm.as_view(), name='picture_delete_form'),
    path('detail/<int:pk>/', PictureDetailView.as_view(), name='picture_detail'),
    path('edit/<int:pk>/', PictureUpdateView.as_view(), name='picture_edit'),
    path('edit_form/<int:pk>/', EditViewByForm.as_view(), name='picture_edit_form'),
    path('edit_updateview/<int:pk>/', EditView.as_view(), name='picture_edit_update'),
    path('check_clean/', CheckValidationView.as_view(), name='picture_clean'),
    path('check_clean_model/', CheckValidationViewByModelForm.as_view(), name='picture_clean_model'),
]