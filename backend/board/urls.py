from django.urls import path
from board.views import *

urlpatterns = [
    path('category/<str:category>/<int:page>', category_list, name='category_list'),
    path('sub_category/<str:sub_category>/<int:page>', sub_category_list, name='sub_category_list'),
    path('tag/<str:tag>/<int:page>', tag_list, name='tag_list'),
]