from utils import task as tasktools
from utils import slurm_api
from analysis.models import *
import json
from utils import sequencepre
import datetime
# Running Success Failed
# import logging

# if complete, data will be update


def procesee_task(taskdetail_dict):
    userpath = taskdetail_dict['userpath']
    sequencepre.phageFastaToCSV(userpath)
    modulelist = taskdetail_dict['modulelist']
    if 'annotation' in modulelist:
        sequencepre.proteindata(userpath)
        sequencepre.upadtephagecsv_genes(userpath)
    for module in modulelist:
        if module == 'quality':
            sequencepre.upadtephagecsv_checkv(userpath)
        if module == 'host':
            sequencepre.updatephagecsv_host(userpath)
        if module == 'lifestyle':
            sequencepre.updatephagecsv_lifestyle(userpath)
        if module == 'trna':
            sequencepre.updatephagecsv_trna(userpath)
        if module == 'anticrispr':
            sequencepre.anticrisprprocess(userpath)
        if module == 'transmembrane':
            sequencepre.transmembraneproprocess(userpath)
        if module == 'taxonomic':
            sequencepre.upadtephagecsv_taxonomy(userpath)


def task_status_update():
    current_time = datetime.datetime.now()
    with open('/home/platform/phage_db/phage_api/workspace/tmp/my_cronjob.log', 'a') as f:
        f.write('exec update start  '+str(current_time)+"\n")
    tasklist = Task.objects.filter(status='Running')

    for task in tasklist:
        try:
            isComplete = False
            taskdetail_dict = json.loads(task.task_detail)
            taskqueue = taskdetail_dict['task_que']
            statuslist = []
            for module in taskqueue:
                if module['job_id'] != '':
                    job_id = int(module['job_id'])
                    module['module_satus'] = slurm_api.get_job_status(job_id)

                    module['module_log']['output'] = slurm_api.get_job_output(
                        job_id)
                    module['module_log']['error'] = slurm_api.get_job_error(job_id)
                    statuslist.append(module['module_satus'])
                else:
                    statuslist.append('Failed')
            for status in statuslist:
                if status != 'COMPLETED':
                    isComplete = False
                    break
                else:
                    isComplete = True
            if isComplete:
                procesee_task(taskdetail_dict)
                task.status = 'Success'
            if 'FAILED' in statuslist:
                task.status = 'Failed'
            task.task_detail = json.dumps(taskdetail_dict)

            task.save()
        except:
            task.status = 'Failed'
            task.task_detail = json.dumps(taskdetail_dict)
            task.save()
            
    with open('/home/platform/phage_db/phage_api/workspace/tmp/my_cronjob.log', 'a') as f:
        f.write('exec update complete  '+str(current_time)+"\n")
    # tasktools.task_status_updata(task, taskdetail_dict)
