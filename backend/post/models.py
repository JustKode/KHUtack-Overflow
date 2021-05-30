from django.db import models
from user.models import User
from board.models import Category, SubCategory
from martor.models import MartorField

class Tag(models.Model):
    tag = models.CharField(max_length=30)
    
    def __str__(self):
        return self.tag


class Comment(models.Model):
    writer = models.ForeignKey(
        User,
        null=True, 
        on_delete=models.SET_NULL
    )
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    writer = models.ForeignKey(
        User,
        null=True, 
        on_delete=models.SET_NULL
    )
    content = MartorField()
    published = models.DateTimeField(auto_now_add=True)
    recommend = models.IntegerField(default=0)


class Question(models.Model):
    title = models.CharField(max_length=100)
    writer = models.ForeignKey(
        User,
        null=True, 
        on_delete=models.SET_NULL
    )
    content = MartorField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(
        SubCategory,
        null=True,
        on_delete=models.SET_NULL
    )
    published = models.DateTimeField(auto_now_add=True)
    recommend = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    comments = models.ManyToManyField(Comment, blank=True)
    answers = models.ManyToManyField(Answer, blank=True)

    def get_comment_count(self):
        return self.comments.all().count()

    def __str__(self):
        return '[' + str(self.category) + '] ' + self.title
