from django.shortcuts import render
from rest_framework.decorators import api_view
from analysis.models import *
from analysis.serializers import *
from rest_framework.response import Response
import random
from plasmid_api import settings
import time
import os
import shutil


# Create your views here.
@api_view(['GET'])
def task_list(request):
    userid = request.query_params.dict()['userid']
    taskslist = Task.objects.filter(user=userid)
    serializer = TaskSerializer(taskslist, many=True)
    return Response({'results': serializer.data})

@api_view(['POST'])
def submit_task(request):
    res = {}

    usertask = str(int(time.time()))+'_' + \
        str(random.randint(1000, 9999))
    uploadfilepath = settings.USERTASKPATH+'/' + \
        usertask + '/upload/'

    os.makedirs(uploadfilepath, exist_ok=False)
    if request.data['rundemo'] == 'true':
        if 'demopath' in request.data:
            shutil.copy(
                settings.DEMOFILE+request.data['demopath'], uploadfilepath+'sequence.fasta')
        else:
            shutil.copy(
                settings.DEMOFILE+"sequence.fasta", uploadfilepath+'sequence.fasta')
        path = uploadfilepath+'sequence.fasta'
    else:
        if request.data['inputtype'] == 'upload':
            file = request.FILES['submitfile']
            path = default_storage.save(
                uploadfilepath+'sequence.fasta', ContentFile(file.read()))
            
        elif request.data['inputtype'] == 'paste':
            path = uploadfilepath+'sequence.fasta'
            with open(path, 'w') as file:
                file.write(request.data['file'])
        else:
            phageids = json.loads(request.data['phageid'])
            path = uploadfilepath+'sequence.fasta'
            tools.searchphagefasta(phageids, path)

    with open(path, 'r') as file:
        # file format check
        is_upload = tools.is_fasta(file)
        if is_upload:
            tools.uploadphagefastapreprocess(path)

            name = request.data['analysistype'] + \
                " " + str(tasks.objects.last().id+1)
            modulejson = json.loads(request.data['modulelist'])
            modulelist = []
            for key, value in modulejson.items():
                if value:
                    modulelist.append(key)
            if 'alignment' in modulelist:
                tools.fixIdLong(path)
            # create task object
            newtask = tasks.objects.create(
                name=name, user=request.data['userid'], uploadpath=usertask,
                analysis_type=request.data['analysistype'], modulelist=modulelist, status='Created')
            userpath = settings.ABSUSERTASKPATH+'/' + usertask
            infodict = {'taskid': newtask.id, 'userpath': userpath, 'modulelist': modulelist,
                        'analysis_type': request.data['analysistype'], 'userid': request.data['userid']}
            taskdetail_dict = task.init_taskdetail_dict(
                infodict)
            newtask.task_detail = json.dumps(taskdetail_dict)
            # run task
            try:
                taskdetail_dict = task.run_annotation_pipline(
                    taskdetail_dict)
                res['status'] = 'Success'
                res['message'] = 'Pipline create successfully'
                res['data'] = {'taskid': newtask.id}
                newtask.task_detail = json.dumps(taskdetail_dict)
                newtask.status = 'Running'
                pass
            except Exception as e:
                res['status'] = 'Failed'
                res['message'] = 'Pipline create failed'
                newtask.status = 'Failed'
                traceback.print_exc()

            newtask.save()

        else:
            res['status'] = 'Failed'
            res['message'] = 'Pipline create failed: The file you uploaded is not a fasta file'
    return Response(res)


