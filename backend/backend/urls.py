"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from retrieve.views import upload
from retrieve.views import returnUploaded
from retrieve.views import main
from ninja import NinjaAPI

api = NinjaAPI()

@api.get("add/")
def add(request, x:float, y:float):
    return main(x,y)

@api.get("getUp/")
def getUp(request):
    return returnUploaded()

@api.post("upload/")
def upload2(request):
    file1 = request.FILES.get("image1")
    file2 = request.FILES.get("image2")
    files = []
    files.append(file1)
    files.append(file2)
    return upload(files)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
