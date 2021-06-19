from django.db import models
from django.utils import timezone
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
    published = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.published:
            self.published = timezone.now()
        return super(Comment, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.writer) + ": " + self.content


class Answer(models.Model):
    writer = models.ForeignKey(
        User,
        null=True, 
        on_delete=models.SET_NULL
    )
    content = MartorField()
    published = models.DateTimeField()
    recommend = models.IntegerField(default=0)
    recommended_person = models.ManyToManyField(User, blank=True, related_name='answer_recommanded_person')
    comments = models.ManyToManyField(Comment, blank=True)

    def save(self, *args, **kwargs):
        if not self.published:
            self.published = timezone.now()
        return super(Answer, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.writer) + ": " + self.content


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
    recommended_person = models.ManyToManyField(User, blank=True, related_name='question_recommanded_person')
    tags = models.ManyToManyField(Tag, blank=True)
    comments = models.ManyToManyField(Comment, blank=True)
    answers = models.ManyToManyField(Answer, blank=True)

    def get_comment_count(self):
        return self.comments.all().count()

    def __str__(self):
        return '[' + str(self.category) + '] ' + self.title
