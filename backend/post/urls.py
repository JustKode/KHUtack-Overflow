from django.urls import path
from post.views import *

urlpatterns = [
    path('question/<int:id>/', get_question, name='get_question'),
    path('question/<int:id>/up_vote/', question_up_vote, name='question_up_vote'),
    path('question/<int:id>/down_vote/', question_down_vote, name='question_down_vote'),
    path('question/<int:id>/comment', post_comment, name='post_comment'),
    path('question/<int:post_id>/comment/put/<int:id>/', put_comment, name='put_comment'),
    path('question/<int:post_id>/comment/delete/<int:id>/', delete_comment, name='delete_comment'),
    path('question/<int:post_id>/answer/', post_answer, name='post_answer'),
    path('question/list/<int:page>', question_list, name='question_list'),
    path('question/write/', post_question, name='post_question')
]