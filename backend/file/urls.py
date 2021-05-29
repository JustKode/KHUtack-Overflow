from django.urls import path
from file import views

urlpatterns = [
    path('uploader/', views.markdown_uploader, name='markdown_uploader_page')
]