from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, Paginator
from board.models import Category, SubCategory
from post.models import Question, Comment, Answer, Tag


def category_list(request, category, page=1):
    category = get_object_or_404(Category, url=category)
    query = request.GET.get('query', None)
    if query == None:
        question_list = Question.objects.filter(category=category)
    else:
        question_list = Question.objects.filter(title__contains=query, category=category) | Question.objects.filter(content__contains=query, category=category) 
    paginator = Paginator(question_list, 10)
    no_result = False
    
    if question_list.count() == 0:
        no_result = True

    if paginator.num_pages < page:
        return render(request, '404.html', {
            "message": "존재하지 않는 페이지 입니다."
        }, status=404)
    
    digit_ten = ((page - 1) // 10 + 1) * 10
    if paginator.num_pages > digit_ten:
        has_next = True
        page_list = [num for num in range(digit_ten - 9, digit_ten + 1)]
    else:
        has_next = False
        page_list = [num for num in range(digit_ten - 9, paginator.num_pages + 1)]

    if page <= 10:
        has_prev = False
    else:
        has_prev = True

    category_list = []
    categories = Category.objects.all()
    for c in categories:
        sub_category = SubCategory.objects.filter(parent=c)
        temp = {
            "category": c,
            "sub_category": sub_category
        }
        category_list.append(temp)

    return render(request, 'question_list_custom.html', {
        'category_list': category_list,
        'title': category.name,
        'questions': paginator.get_page(page),
        'dynamic_url': 'category',
        'dynamic_query': category.url,
        'query': query,
        'page': page,
        'has_next': has_next,
        'has_prev': has_prev,
        'prev': page_list[0] - 1,
        'next': page_list[-1] + 1,
        'page_list': page_list,
        'no_result': no_result
    })

def sub_category_list(request, sub_category, page=1):
    sub_category = get_object_or_404(SubCategory, url=sub_category)
    query = request.GET.get('query', None)
    if query == None:
        question_list = Question.objects.filter(sub_category=sub_category)
    else:
        question_list = Question.objects.filter(title__contains=query, sub_category=sub_category) | Question.objects.filter(content__contains=query, sub_category=sub_category) 
    paginator = Paginator(question_list, 10)
    no_result = False
    
    if question_list.count() == 0:
        no_result = True

    if paginator.num_pages < page:
        return render(request, '404.html', {
            "message": "존재하지 않는 페이지 입니다."
        }, status=404)
    
    digit_ten = ((page - 1) // 10 + 1) * 10
    if paginator.num_pages > digit_ten:
        has_next = True
        page_list = [num for num in range(digit_ten - 9, digit_ten + 1)]
    else:
        has_next = False
        page_list = [num for num in range(digit_ten - 9, paginator.num_pages + 1)]

    if page <= 10:
        has_prev = False
    else:
        has_prev = True

    category_list = []
    categories = Category.objects.all()
    for c in categories:
        sub_c = SubCategory.objects.filter(parent=c)
        temp = {
            "category": c,
            "sub_category": sub_c
        }
        category_list.append(temp)


    return render(request, 'question_list_custom.html', {
        'category_list': category_list,
        'title': sub_category.name,
        'questions': paginator.get_page(page),
        'dynamic_url': 'sub_category',
        'dynamic_query': sub_category.url,
        'query': query,
        'page': page,
        'has_next': has_next,
        'has_prev': has_prev,
        'prev': page_list[0] - 1,
        'next': page_list[-1] + 1,
        'page_list': page_list,
        'no_result': no_result
    })

def tag_list(request, tag, page=1):
    tag = get_object_or_404(Tag, tag=tag)
    query = request.GET.get('query', None)
    if query == None:
        question_list = Question.objects.filter(tags=tag)
    else:
        question_list = Question.objects.filter(title__contains=query, tags=tag) | Question.objects.filter(content__contains=query, tags=tag) 
    paginator = Paginator(question_list, 10)
    no_result = False
    
    if question_list.count() == 0:
        no_result = True

    if paginator.num_pages < page:
        return render(request, '404.html', {
            "message": "존재하지 않는 페이지 입니다."
        }, status=404)
    
    digit_ten = ((page - 1) // 10 + 1) * 10
    if paginator.num_pages > digit_ten:
        has_next = True
        page_list = [num for num in range(digit_ten - 9, digit_ten + 1)]
    else:
        has_next = False
        page_list = [num for num in range(digit_ten - 9, paginator.num_pages + 1)]

    if page <= 10:
        has_prev = False
    else:
        has_prev = True

    category_list = []
    categories = Category.objects.all()
    for c in categories:
        sub_c = SubCategory.objects.filter(parent=c)
        temp = {
            "category": c,
            "sub_category": sub_c
        }
        category_list.append(temp)


    return render(request, 'question_list_custom.html', {
        'category_list': category_list,
        'title': '#' + tag.tag,
        'questions': paginator.get_page(page),
        'dynamic_url': 'tag',
        'dynamic_query': tag.tag,
        'query': query,
        'page': page,
        'has_next': has_next,
        'has_prev': has_prev,
        'prev': page_list[0] - 1,
        'next': page_list[-1] + 1,
        'page_list': page_list,
        'no_result': no_result
    })