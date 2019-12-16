
from django.db import models
from django.utils import timezone


class History(models.Model):
    user = models.CharField(max_length=200)
    name = models.CharField(max_length=200 , default = "Без названия")
    criterian = models.CharField(max_length=200)
    variants = models.CharField(max_length=200)
    selection_result = models.CharField(max_length=500)
    selection_add = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return '{}'.format(self.name , self.user, self.criterian)


