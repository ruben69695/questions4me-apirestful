from django.db import models

# Create your models here.
class Question(models.Model):
    created_by = models.CharField(max_length=90, blank=True, null=True)
    content = models.TextField(max_length=600)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    answered_at = models.DateTimeField(blank=True, null=True)