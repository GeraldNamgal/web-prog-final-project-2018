from django.db import models
from django.contrib.auth.models import User

class MemoCategory(models.Model):
    userID = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{User.objects.get(pk=self.userID).username} (userID# {self.userID}) \
            has Memo Category "{self.name}"'

class Memo(models.Model):
    userID = models.IntegerField()
    name = models.CharField(max_length=64)
    category = models.ForeignKey(MemoCategory, on_delete=models.SET_NULL, null=True, blank=True)
    day = models.DateField()
    startTime = models.TimeField(null=True, blank=True)
    endTime = models.TimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{User.objects.get(pk=self.userID).username} (userID# {self.userID}) \
            made Memo "{self.name}" [{self.day}], Start Time = [{self.startTime}], Category = [{self.category}]'
