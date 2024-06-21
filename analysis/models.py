from django.db import models

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    user = models.CharField(max_length=300, blank=True, null=True)
    uploadpath = models.CharField(max_length=200, blank=True, null=True)
    analysis_type = models.CharField(max_length=60, blank=True, null=True)
    modulelist = models.CharField(max_length=400, blank=True, null=True)
    status = models.CharField(max_length=60, blank=True, null=True)
    task_log = models.TextField(blank=True, null=True)
    task_detail = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)