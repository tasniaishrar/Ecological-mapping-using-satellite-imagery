from django.urls import path
from . import views

app_name = "retrieve"
urlpatterns = [
    path(r'', views.pre_post_disaster_img, name='pre_post_disaster_img'),
]