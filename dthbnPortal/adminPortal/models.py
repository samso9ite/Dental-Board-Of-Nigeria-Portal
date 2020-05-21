from django.db import models
from authentication.models import User
from schPortal.models import Indexing

# Create your models here.


class IndexLimit(models.Model):
    school = models.ForeignKey(User, on_delete=models.CASCADE)
    # index_instance = models.ForeignKey(Indexing, on_delete=models.CASCADE, related_name='index_record', null=True)
    assigned_limit = models.CharField(max_length=40)
    used_limit = models.IntegerField()

    def __str__(self):
        return self.assigned_limit


class Restrictions(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    block = models.BooleanField(default=False)
    suspend = models.BooleanField(default=False)

    