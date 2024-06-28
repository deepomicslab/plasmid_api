from rest_framework import serializers
from analysis.models import *


class TaskSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Task
        fields = ['id','name', 'user', 'uploadpath', 'analysis_type', 'modulelist', 'status', 'task_log', 'task_detail', 'created_at']