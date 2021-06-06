from django.db import models

class Statuses(models.Model):
    name = models.CharField(max_length=20, unique=True)
    add_date = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name
