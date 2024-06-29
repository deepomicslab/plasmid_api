from django.shortcuts import render
from rest_framework.decorators import api_view
from database.models import *
from analysis.models import *
from analysis.serializers import *
from rest_framework.response import Response
import random
from plasmid_api import settings
import time
import os
import shutil
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
from utils import tools, task, slurm_api
import traceback
import csv
import pandas as pd
from django.http import FileResponse


# Create your views here.
@api_view(['GET'])
def task_list(request):
    userid = request.query_params.dict()['userid']
    taskslist = Task.objects.filter(user=userid).order_by('-created_at')
    serializer = TaskSerializer(taskslist, many=True)
    return Response({'results': serializer.data})

@api_view(['POST'])
def check_plasmid_ids(request):
    res = {}
    
    split_plasmidids = request.data['plasmidids'].split(';')
    search_pids=[]
    phages = Plasmid.objects.filter(plasmid_id__in=split_plasmidids)
    for ph in phages:
        search_pids.append(ph.plasmid_id)
    #       idlist.value = res.idlist
    # inputfeedback.value = res.message
    # validationstatus.value = res.status

    res['idlist']=search_pids
    res['message']='Your selected phage ids are valid: '+', '.join(search_pids)
    res['status']='success'
    return Response(res)

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
                settings.DEMOFILE+"plasmid.fasta", uploadfilepath+'sequence.fasta')
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

            if Task.objects.all().count() == 0:
                name = request.data['analysistype'] + \
                    " " + str(1)
            else:
                name = request.data['analysistype'] + \
                    " " + str(Task.objects.last().id+1)
            modulejson = json.loads(request.data['modulelist'])
            modulelist = []
            for key, value in modulejson.items():
                if value:
                    modulelist.append(key)
            if 'alignment' in modulelist:
                tools.fixIdLong(path)
            # create task object
            newtask = Task.objects.create(
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

def submit_cluster_task(request):
    res = {}
    usertask = str(int(time.time()))+'_' + \
        str(random.randint(1000, 9999))
    uploadfilepath = settings.USERTASKPATH+'/' + \
        usertask + '/upload/'
    os.makedirs(uploadfilepath, exist_ok=False)
    if request.data['rundemo'] == 'true':
        ##!!!need to use settings_local config
        shutil.copy(
            settings.DEMOFILE+"plasmid.fasta", uploadfilepath+'sequence.fasta')
        path = uploadfilepath+'sequence.fasta'
    else:
        if request.data['inputtype'] == 'upload':
            file = request.FILES['submitfile']
            path = default_storage.save(
                uploadfilepath+'sequence.fasta', ContentFile(file.read()))
            
        #request.data['inputtype'] == 'paste'
        else :
            path = uploadfilepath+'sequence.fasta'
            with open(path, 'w') as file:
                file.write(request.data['file'])
            

    with open(path, 'r') as file:
        # file format check
        is_upload = tools.is_fasta(path)
        if is_upload:
            is_multi = tools.is_multifasta(path)
            if is_multi:
                tools.uploadphagefastapreprocess(path)
                if Task.objects.all().count() == 0:
                    name = request.data['analysistype'] + \
                        " " + str(1)
                else:
                    name = request.data['analysistype'] + \
                        " " + str(Task.objects.last().id+1)
                
                modulejson = json.loads(request.data['modulelist'])
                modulelist = []
                for key, value in modulejson.items():
                    if value:
                        modulelist.append(key)
                # create task object
                newtask = Task.objects.create(
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
                    taskdetail_dict = task.run_cluster_pipline(
                        taskdetail_dict)
                    res['status'] = 'Success'
                    res['message'] = 'Pipline create successfully'
                    res['data'] = {'taskid': newtask.id}
                    print(taskdetail_dict)
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
                res['message'] = 'The number of file sequences you uploaded is less than 2.'

        else:
            res['status'] = 'Failed'
            res['message'] = 'Pipline create failed: The file you uploaded is not a fasta file'
    return Response(res)

@api_view(['GET'])
def view_task_detail(request):
    # userid = request.query_params.dict()['userid']
    taskid = request.query_params.dict()['taskid']

    # taskslist = tasks.objects.filter(user=userid, id=taskid)
    taskslist = Task.objects.filter(id=taskid).order_by('-created_at')
    serializer = TaskSerializer(taskslist, many=True)
    return Response({'results': serializer.data[0]})

@api_view(['GET'])
def view_task_log(request):
    # userid = request.query_params.dict()['userid']
    taskid = request.query_params.dict()['taskid']
    moudlename = request.query_params.dict()['moudlename']
    task_object = Task.objects.get(id=taskid)
    task_detail=json.loads(task_object.task_detail)
    job_id=None
    for module in  task_detail['task_que']:
        if module['module']==moudlename:
            job_id=module['job_id']
            break
    task_log='no log'
    task_error='no log'
    if job_id != None:
        task_log=slurm_api.get_job_output(job_id)
        task_error=slurm_api.get_job_error(job_id)
    return Response({'task_log': task_log,'task_error':task_error})

@api_view(['GET'])
def view_task_result(request):
    taskid = request.query_params.dict()['taskid']
    task = Task.objects.get(id=taskid)
    path = settings.USERTASKPATH+'/' + \
        task.uploadpath+'/output/result/phage.tsv'

    phagelist = []
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for id, row in enumerate(reader):
            dictr = dict(row)
            dictr['id'] = id+1
            phagelist.append(dictr)
    return Response({'results': phagelist})

@api_view(['GET'])
def view_task_result_proteins(request):
    params_dict=request.query_params.dict()
    taskid = request.query_params.dict()['taskid']
    task = Task.objects.get(id=taskid)
    path = settings.USERTASKPATH+'/' + \
            task.uploadpath+'/output/result/protein.tsv'
    if 'phageid' in params_dict:
        phageid = request.query_params.dict()['phageid']
        proteins = pd.read_csv(path, sep='\t', index_col=False)
        proteins['phageid']=proteins['phageid'].astype(str)
        proteindict = proteins[proteins['phageid']
                            == phageid].to_dict(orient='records')
        return Response({'results': proteindict})
    else:
        proteins = pd.read_csv(path, sep='\t', index_col=False)
        #for heatmap
        proteindict =  proteins[['Protein_id', 'phageid','Protein_function_classification']].to_dict(orient='records')
        return Response({'results': proteindict})

@api_view(['GET'])
def view_task_result_plasmid_detail(request):
    taskid = request.query_params.dict()['taskid']
    phageid = request.query_params.dict()['phageid']
    task = Task.objects.get(id=taskid)
    path = settings.USERTASKPATH+'/' + \
        task.uploadpath+'/output/result/phage.tsv'
    phages = pd.read_csv(path, sep='\t', index_col=False)
    phage = phages[phages['Acession_ID'] == phageid].to_dict(orient='records')
    return Response({'results': phage[0]})

@api_view(['GET'])
def view_task_result_plasmid_fasta(request):
    taskid = request.query_params.dict()['taskid']
    phageid = request.query_params.dict()['phageid']
    task = Task.objects.get(id=taskid)
    path = settings.USERTASKPATH+'/' + \
        task.uploadpath+'/output/result/' + phageid + '/sequence.fasta'
    file = open(path, 'rb')
    response = FileResponse(file)
    response['Content-Disposition'] = 'attachment; filename="sequence.fasta"'
    response['Content-Type'] = 'text/plain'
    return response

@api_view(['GET'])
def download_task_result_output_file(request, path):
    file_path = settings.USERTASKPATH + '/' + path
    file = open(file_path, 'rb')
    response = FileResponse(file)
    filename = file.name.split('/')[-1]
    response['Content-Disposition'] = "attachment; filename="+filename
    response['Content-Type'] = 'text/plain'
    return response