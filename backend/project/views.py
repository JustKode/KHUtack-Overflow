from django.core import paginator
from django.shortcuts import render
from django.core.paginator import Paginator
from post.models import Question

def main(request):
    question_list = Question.objects.all()
    paginator = Paginator(question_list, 5)
    return render(request, 'index.html', {'questions': paginator.get_page(1)})