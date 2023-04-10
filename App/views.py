import json

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Imaginary function to handle an uploaded file.

from django.shortcuts import render

from App.consumers import base64_to_image
from App.face_save_mysql.face_save_image import face_save_image


# from .forms import ModelFormWithFileField
#
# def upload_file(request):
#     if request.method == 'POST':
#         form = ModelFormWithFileField(request.POST, request.FILES)
#         if form.is_valid():
#             # file is saved
#             form.save()
#             return HttpResponseRedirect('/success/url/')
#     else:
#         form = ModelFormWithFileField()
#     return render(request, 'upload.html', {'form': form})
#
# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             return HttpResponse("succeed")
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def Video(request):
    return render(request, 'Video.html')


def home(request):
    return render(request, 'Home.html')


def faceEntering(request):
    return render(request, 'faceEntering.html')


def faceRecognition(request):
    return render(request, 'faceRecognition.html')


@csrf_exempt
def Test(request):
    if request.method == "GET":
        print(request.GET.get("name"))
        return HttpResponse("你好呀");


def IdentifyFace(imgData):
    result = ""
    return result


# 保存用户数据 path:'/PostUserData'
def PostUserData(request):
    if request.method == "POST":

        jsonData = json.loads(request.body)
        username = jsonData['username']
        img = jsonData['faceImg']
        img = base64_to_image(img)
        imgList=[]
        imgList.append(img)
        result = SaveUserData(username, imgList)
        return HttpResponse(result)
        # print(jsonData)
        # return HttpResponse(jsonData['username'])
    else:
        return HttpResponse("No This Request")



def SaveUserData(username, imgData):
    # result = "username:"+str(username)
    result=face_save_image(username,imgData)
    return result

