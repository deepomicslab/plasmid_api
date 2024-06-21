from rest_framework import serializers
from analysis.models import *


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id','name', 'user', 'uploadpath', 'analysis_type', 'modulelist', 'status', 'task_log', 'created_at']

