from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, Paginator
from board.models import Category, SubCategory
from post.models import Question, Comment, Answer, Tag
from post.forms import PostForm
import json


def get_question(request, id):
    if request.method == 'GET':
        question = get_object_or_404(Question, pk=id)
        form = PostForm()
        return render(request, 'question.html', {'question': question, 'form': form, 'tags': question.tags.all()})


def post_question(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        body = request.POST
        if body.get('title', None) == None:
            messages.error(request, '제목을 입력 해 주세요.')
            return redirect('post_question')
        elif body.get('main_category', '-') == '-':
            messages.error(request, "카테고리를 선택 해 주세요.")
            return redirect('post_question')
        elif body.get('content', None) == None:
            messages.error(request, "내용을 입력 해 주세요.")
            return redirect('post_question')
        
        data = {
            "title": body['title'],
            "writer": request.user,
            "content": body['content'],
            "category": Category.objects.get(name=body['main_category'])
        }
        if body.get('sub_category', '-') != '-':
            data['sub_category'] = SubCategory.objects.get(name=body['sub_category'])

        question = Question.objects.create(**data)
        for tag_name in body.getlist('tag[]'):
            try:
                tag = Tag.objects.get(tag=tag_name)
                question.tags.add(tag)
            except Tag.DoesNotExist:
                tag = Tag.objects.create(tag=tag_name)
                tag.save()
                question.tags.add(tag)

        question.save()
        messages.success(request, '성공적으로 답변을 작성하였습니다.')
        return redirect('get_question', id=question.id)
    else:
        form = PostForm()
        category_list = [{"category": "-", "sub_category": ["-"]}]
        categories = Category.objects.all()
        for category in categories:
            sub_category = SubCategory.objects.filter(parent=category)
            temp = {
                "category": category.name,
                "sub_category": ['-'] + [e.name for e in sub_category]
            }
            category_list.append(temp)
        return render(request, 'question_write.html', {'form': form, 'category_list': json.dumps(category_list)})


def delete_question(request, id):
    question = get_object_or_404(Question, pk=id)
    if question.writer != request.user:
        messages.error(request, "본인의 글만 삭제 가능합니다.")
        return redirect('get_question', id)
    else:
        question.delete()
        messages.success(request, "게시글을 삭제 하는데에 성공 하였습니다.")
        return redirect('question_list', 1)


def put_question(request, id):
    question = get_object_or_404(Question, pk=id)
    if question.writer != request.user:
        messages.error(request, "본인의 글만 수정 가능합니다.")
        return redirect('get_question', id)
    
    if request.method == 'POST':
        body = request.POST
        if body.get('title', None) == None:
            messages.error(request, '제목을 입력 해 주세요.')
            return redirect('post_question')
        elif body.get('main_category', '-') == '-':
            messages.error(request, "카테고리를 선택 해 주세요.")
            return redirect('post_question')
        elif body.get('content', None) == None:
            messages.error(request, "내용을 입력 해 주세요.")
            return redirect('post_question')

        question.title = body['title']
        question.content = body['content']
        question.category = Category.objects.get(name=body['main_category'])
        if body.get('sub_category', '-') != '-':
            question.sub_category = SubCategory.objects.get(name=body['sub_category'])
        question.tags.clear()

        for tag_name in body.getlist('tag[]'):
            try:
                tag = Tag.objects.get(tag=tag_name)
                question.tags.add(tag)
            except Tag.DoesNotExist:
                tag = Tag.objects.create(tag=tag_name)
                tag.save()
                question.tags.add(tag)

        question.save()
        messages.success(request, "정보 수정에 성공하였습니다!")
        return redirect('get_question', id=question.id)
    else:
        form = PostForm()
        category_list = [{"category": "-", "sub_category": ["-"]}]
        categories = Category.objects.all()
        for category in categories:
            sub_category = SubCategory.objects.filter(parent=category)
            temp = {
                "category": category.name,
                "sub_category": ['-'] + [e.name for e in sub_category]
            }
            category_list.append(temp)

        if question.sub_category == None:
            sub_category = '-'
        else:
            sub_category = question.sub_category.name
        
        return render(request, 'question_modify.html', {
            'form': form,
            'id': id,
            'category_list': json.dumps(category_list),
            'title': question.title,
            'content': question.content,
            'tags': question.tags.all(),
            'main_category': question.category.name,
            'sub_category': sub_category
        })

        
def question_up_vote(request, id):
    if request.method == 'GET':
        question = get_object_or_404(Question, pk=id)

        if request.user not in question.recommended_person.all():
            question.recommended_person.add(request.user)
            question.recommend += 1
            question.writer.points += 1
            question.save()
            question.writer.save()
        else:
            messages.error(request, '이미 추천 하셨습니다.')
        
        return redirect('get_question', id=id)


def question_down_vote(request, id):
    if request.method == 'GET':
        question = get_object_or_404(Question, pk=id)

        if request.user not in question.recommended_person.all():
            question.recommended_person.add(request.user)
            question.recommend -= 1
            question.save()
        else:
            messages.error(request, '이미 추천 하셨습니다.')
        
        return redirect('get_question', id=id)


def answer_up_vote(request, id):
    if request.method == 'GET':
        answer = get_object_or_404(Answer, pk=id)

        if request.user not in answer.recommended_person.all():
            answer.recommended_person.add(request.user)
            answer.recommend += 1
            answer.writer.points += 1
            answer.save()
            answer.writer.save()
        else:
            messages.error(request, '이미 추천 하셨습니다.')
        
        return redirect('get_question', id=Question.objects.get(answers=answer).id)


def answer_down_vote(request, id):
    if request.method == 'GET':
        answer = get_object_or_404(Answer, pk=id)

        if request.user not in answer.recommended_person.all():
            answer.recommended_person.add(request.user)
            answer.recommend -= 1
            answer.save()
        else:
            messages.error(request, '이미 추천 하셨습니다.')
        
        return redirect('get_question', id=Question.objects.get(answers=answer).id)


def post_comment(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        question = get_object_or_404(Question, pk=id)
        content = request.POST.get('comment')

        if content == '':
            messages.error(request, '내용을 입력 해 주세요.')
            return redirect('get_question', id=id)
        
        comment = Comment(writer=request.user, content=content)
        comment.save()
        question.comments.add(comment)

        messages.success(request, '성공적으로 댓글을 작성 하였습니다.')
        return redirect('get_question', id=id)
    else:
        messages.error(request, '잘못 된 접근 입니다.')
        return redirect('get_question', id=id)


def put_comment(request, post_id, id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=id)
        content = request.POST.get('content')

        if content == '':
            messages.error(request, '내용을 입력 해 주세요.')
            return redirect('get_question', id=post_id)
        elif comment.writer != request.user:
            messages.error(request, '본인의 글만 수정 할 수 있습니다.')
            return redirect('get_question', id=post_id)
        
        comment.content = content
        comment.save()

        messages.success(request, '성공적으로 댓글을 수정완료 하였습니다.')
        return redirect('get_question', id=post_id)
    else:
        messages.error(request, '잘못 된 접근 입니다.')
        return redirect('get_question', id=post_id)


def delete_comment(request, post_id, id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=id)
        if comment.writer != request.user:
            messages.error(request, '본인의 글만 삭제 할 수 있습니다.')
            return redirect('get_question', id=post_id)
        comment.delete()

        messages.success(request, '성공적으로 댓글을 삭제 하였습니다.')
        return redirect('get_question', id=post_id)
    else:
        messages.error(request, '잘못 된 접근 입니다.')
        return redirect('get_question', id=post_id)


def post_answer_comment(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    answer = get_object_or_404(Answer, pk=id)
    if request.method == 'POST':
        content = request.POST.get('comment')

        if content == '':
            messages.error(request, '내용을 입력 해 주세요.')
            return redirect('get_question', id=id)
        
        comment = Comment(writer=request.user, content=content)
        comment.save()
        answer.comments.add(comment)

        messages.success(request, '성공적으로 댓글을 작성 하였습니다.')
        return redirect('get_question', id=Question.objects.get(answers=answer).id)
    else:
        messages.error(request, '잘못 된 접근 입니다.')
        return redirect('get_question', id=Question.objects.get(answers=answer).id)


def post_answer(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        question = get_object_or_404(Question, pk=post_id)
        content = request.POST.get('content')

        if content == '':
            messages.error(request, '내용을 입력 해 주세요.')
            return redirect('get_question', id=post_id)
        
        answer = Answer(writer=request.user, content=content)
        answer.save()
        question.answers.add(answer)

        messages.success(request, '성공적으로 답변을 작성하였습니다.')
        return redirect('get_question', id=post_id)
    else:
        messages.error(request, '잘못 된 접근 입니다.')
        return redirect('get_questsion', id=post_id)


def put_answer(request, id):
    answer = get_object_or_404(Answer, pk=id)
    if answer.writer != request.user:
        messages.error(request, "본인 글만 수정 할 수 있습니다.")
        return redirect('get_question', Question.objects.get(answers=answer).id)

    if request.method == 'POST':
        body = request.POST
        if body.get('content', None) == None:
            messages.error(request, "내용을 입력 해 주세요.")
            return redirect('post_question')

        answer.content = body['content']
        answer.save()
        messages.success(request, "정보 수정에 성공하였습니다!")
        return redirect('get_question', Question.objects.get(answers=answer).id)
    else:
        form = PostForm()
        return render(request, 'answer_modify.html', {
            'form': form,
            'id': id,
            'content': answer.content
        })


def delete_answer(request, id):
    answer = get_object_or_404(Answer, pk=id)
    if answer.writer != request.user:
        messages.error(request, "본인 글만 삭제 할 수 있습니다.")
        return redirect('get_question', Question.objects.get(answers=answer).id)
    else:
        question = Question.objects.get(answers=answer)
        answer.delete()
        messages.success(request, "성공적으로 글을 삭제 하였습니다.")
        return redirect('get_question', question.id)


def question_list(request, page=1):
    query = request.GET.get('query', None)
    if query == None:
        question_list = Question.objects.all().order_by('-published')
    else:
        question_list = (Question.objects.filter(title__contains=query) | Question.objects.filter(content__contains=query)).order_by('-published')
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

    # category
    category_list = []
    categories = Category.objects.all()
    for category in categories:
        sub_category = SubCategory.objects.filter(parent=category)
        temp = {
            "category": category,
            "sub_category": sub_category
        }
        category_list.append(temp)


    return render(request, 'question_list.html', {
        'category_list': category_list,
        'questions': paginator.get_page(page),
        'query': query,
        'page': page,
        'has_next': has_next,
        'has_prev': has_prev,
        'prev': page_list[0] - 1,
        'next': page_list[-1] + 1,
        'page_list': page_list,
        'no_result': no_result
    })