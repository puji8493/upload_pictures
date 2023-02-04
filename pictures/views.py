from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView,ListView
from .models import UploadFile
from .forms import UploadForm


class PictureCreateView(CreateView):
    model = UploadFile
    fields = '__all__'
    template_name = 'index.html'
    success_url = reverse_lazy('pictures:list')

    def get(self,request,*args,**kwargs):
        context = {
            'title':"画像のアップロード",
            'upload_form':UploadForm(),
            'id':None,
        }
        return render(request,'index.html',context)

    def post(self, request, *args, **kwargs):
        # 画像をアップロードする処理を書く
        upload_form = UploadForm(request.POST or None, request.FILES or None)
        if upload_form.is_valid() and request.FILES:
            upload_image = upload_form.save()
        return render(request,'home.html',context={'id': upload_image.id})

class PictureList(ListView):
    model = UploadFile
    template_name = 'list.html'


# class IndexView(View):
#
#     def get(self,request,*args,**kwargs):
#         context = {
#             'title':"画像のアップロード",
#             'upload_form':UploadForm(),
#             'id':None,
#         }
#         return render(request,'index.html',context)
#
#     def post(self,request,*args,**kwargs):
#         upload_form = UploadForm(request.POST,request.FILES)
#         if upload_form.is_valid():
#             upload_image = upload_form.save()
#
#         return render(request,'index.html',context={'id': upload_image.id})
