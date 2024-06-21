from django.shortcuts import render
from rest_framework.decorators import api_view
from analysis.models import *
from analysis.serializers import *
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
def viewtask(request):
    userid = request.query_params.dict()['userid']
    taskslist = Task.objects.filter(user=userid)
    serializer = TaskSerializer(taskslist, many=True)
    return Response({'results': serializer.data})