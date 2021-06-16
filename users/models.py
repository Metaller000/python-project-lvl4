from django.db import models
from django.contrib.auth.models import User


class Statuses(models.Model):
    name = models.CharField(max_length=20, unique=True)
    add_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name

class Labels(models.Model):
    name = models.CharField(max_length=20, unique=True)
    add_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name

class Tasks(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=500, null=True)
    autor = models.CharField(max_length=20)
    add_date = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.ForeignKey(Statuses, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)    
    label = models.ManyToManyField(Labels)

    def __str__(self):
        return self.name


