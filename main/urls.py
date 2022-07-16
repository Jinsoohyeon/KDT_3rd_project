from django.urls import path
from .views import index, about, post, contact, chart_data,prediction, recommend

app_name = "main"
urlpatterns = [
    path('', index , name='index'),
    path('tour2/', about , name='about'),
    # path('tour3/', post , name='post'),
    path('tour3/', chart_data , name='post'),
    path('tour4/', contact , name='contact'),
    path('recommend/', recommend , name='recommend'),
    ]
    