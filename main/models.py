# Create your models here.

from django.db import models
from django.utils.timezone import now

# Create your models here.

class TripNews(models.Model):
    news_url = models.CharField(max_length=200, unique=True,  default='')
    title = models.CharField(max_length=200, default='')
    loc = models.CharField(max_length=100,  default='')
    date = models.CharField(max_length=10,  default='')
    likeCnt = models.CharField(max_length=10, null=True)
    shareCnt = models.CharField(max_length=10, null=True)
    readCnt = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.title}--{self.loc}--{self.date}--{self.created_at}'

class NewsSummery(models.Model):
    post_url = models.CharField(max_length=200, null=True)
    card_title = models.CharField(max_length=100, null=True)
    summary_info = models.CharField(max_length=10000, null=True)
    img_url = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.pk}--{self.card_title}'

class InputKeyword(models.Model) :
    keyword = models.CharField(max_length=100)
    count = models.IntegerField()