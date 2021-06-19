from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from post.models import Question, Comment, Answer
from post.forms import PostForm


def get_question(request, id):
    if request.method == 'GET':
        question = get_object_or_404(Question, pk=id)
        form = PostForm()
        return render(request, 'question.html', {'question': question, 'form': form})


def question_up_vote(request, id):
    if request.method == 'GET':
        question = get_object_or_404(Question, pk=id)

        if request.user not in question.recommended_person.all():
            question.recommended_person.add(request.user)
            question.recommend += 1
            question.save()
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
