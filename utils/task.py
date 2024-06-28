from plasmid_api import settings
from utils import slurm_api
import json
# annotation: false,
# quality: false,
# host: false,
# lifestyle: false,
# trna: false,
# anticrispr: false,
# crisprcas: false,
# transmembrane: false,
# terminator

#    infodict = {'taskid': newtask.id, 'userpath': usertask, 'modulelist': modulelist,
#                 'analysis_type': request.data['analysistype'], 'userid': request.data['userid']}

##### run analysis script#####


def init_taskdetail_dict(info_dict):
    new_dict = {}
    new_dict["taskid"] = info_dict["taskid"]
    new_dict["userpath"] = info_dict["userpath"]
    new_dict["task_status"] = "create"
    module_list = info_dict["modulelist"]
    new_dict["modulelist"] = module_list
    new_dict["analysis_type"] = info_dict["analysis_type"]
    new_dict["userid"] = info_dict["userid"]

    task_que = []
    if 'transmembrane' in module_list and 'annotation' not in module_list:
        new_dict["log"] = "Transmembrane Protein Annotation must need ORF prediction & Protein classification"
        new_dict["status"] = "error"

    if 'terminator' in module_list and 'annotation' not in module_list:
        new_dict["log"] = "Transcription Terminator Annotation must need ORF prediction & Protein classification"
        new_dict["status"] = "error"

    if 'anticrispr' in module_list and 'annotation' not in module_list:
        new_dict["log"] = "Anti-CRISPR Protein Annotation must need ORF prediction & Protein classification"
        new_dict["status"] = "error"
    
    # annotation must be the first module
    if 'annotation' in module_list:
        task_dict = {'module': 'annotation',
                     'module_satus': 'waiting', 'job_id': '', 'module_log': {'output': '', 'error': ''}}
        task_que.append(task_dict)
    for module in module_list:
        if module == 'annotation':
            continue
        task_dict = {'module': module,
                     'module_satus': 'waiting', 'job_id': '', 'module_log': {'output': '', 'error': ''}}
        task_que.append(task_dict)
    new_dict["task_que"] = task_que
    return new_dict

# first run task and update task status
def update_task_que(taskdetail_dict, module, status, job_id):
    for task in taskdetail_dict["task_que"]:
        if task["module"] == module:
            task["module_satus"] = status
            task["job_id"] = job_id
    return taskdetail_dict


def run_annotation(taskdetail_dict):
    # sbatch /home/platform/phage_db/phage_api/workspace/analysis_script/annotation/run.sh /home/platform/phage_db/phage_api/workspace/user_task/sequence.fasta /home/platform/phage_db/phage_api/workspace/user_task/output
    userpath = taskdetail_dict["userpath"]
    inputpath = userpath + "/upload/sequence.fasta"
    outputpath = userpath + "/output/rawdata/annotation"
    shell_script = settings.ANALYSIS + "annotation_v2/run.sh"
    script_arguments = [inputpath, outputpath]
    #shell_script = "/home/platform/phage_db/phage_api/workspace/analysis_script/annotation/run.sh"
    job_id = slurm_api.submit_job(
        shell_script, script_arguments=script_arguments)
    status = slurm_api.get_job_status(job_id)
    taskdetail_dict = update_task_que(
        taskdetail_dict, "annotation", status, job_id)
    return taskdetail_dict


def run_quality(taskdetail_dict):
    # sbatch /home/platform/phage_db/phage_api/workspace/analysis_script/quality/run.sh /home/platform/phage_db/phage_api/workspace/user_task/sequence.fasta /home/platform/phage_db/phage_api/workspace/user_task/output
    userpath = taskdetail_dict["userpath"]
    inputpath = userpath + "/upload/sequence.fasta"
    outputpath = userpath + "/output/rawdata/quality"
    shell_script = settings.ANALYSIS + "quality/run.sh"
    script_arguments = [inputpath, outputpath]
    shell_script = "/home/platform/phage_db/phage_api/workspace/analysis_script/quality/run.sh"
    job_id = slurm_api.submit_job(
        shell_script, script_arguments=script_arguments)
    status = slurm_api.get_job_status(job_id)
    taskdetail_dict = update_task_que(
        taskdetail_dict, "quality", status, job_id)
    return taskdetail_dict


def run_host(taskdetail_dict):
    # sbatch /home/platform/phage_db/phage_api/workspace/analysis_script/host/run.sh /home/platform/phage_db/phage_api/workspace/user_task/sequence.fasta /home/platform/phage_db/phage_api/workspace/user_task/output
    userpath = taskdetail_dict["userpath"]
    inputpath = userpath + "/upload/sequence.fasta"
    outputpath = userpath + "/output/rawdata/host"
    shell_script = settings.ANALYSIS + "host/run.sh"
    script_arguments = [inputpath, outputpath]
    shell_script = "/home/platform/phage_db/phage_api/workspace/analysis_script/host/run.sh"
    job_id = slurm_api.submit_job(
        shell_script, script_arguments=script_arguments)
    status = slurm_api.get_job_status(job_id)
    taskdetail_dict = update_task_que(
        taskdetail_dict, "host", status, job_id)
    return taskdetail_dict


def run_lifestyle(taskdetail_dict):
    # sbatch /home/platform/phage_db/phage_api/workspace/analysis_script/lifestyle/run.sh /home/platform/phage_db/phage_api/workspace/user_task/sequence.fasta /home/platform/phage_db/phage_api/workspace/user_task/output
    userpath = taskdetail_dict["userpath"]
    inputpath = userpath + "/upload/sequence.fasta"
    outputpath = userpath + "/output/rawdata/lifestyle/result.txt"
    outputpathdir = userpath + "/output/rawdata/lifestyle"
    shell_script = settings.ANALYSIS + "lifestyle/run.sh"
    script_arguments = [inputpath, outputpath, outputpathdir]
    shell_script = "/home/platform/phage_db/phage_api/workspace/analysis_script/lifestyle/run.sh"
    job_id = slurm_api.submit_job(
        shell_script, script_arguments=script_arguments)
    status = slurm_api.get_job_status(job_id)
    taskdetail_dict = update_task_que(
        taskdetail_dict, "lifestyle", status, job_id)
    return taskdetail_dict


def run_transmembrane(taskdetail_dict):
    userpath = taskdetail_dict["userpath"]
    inputpath = userpath + "/output/rawdata/annotation/gene.faa"
    outputpath = userpath + "/output/rawdata/transmembrane/result.txt"
    outputpathdir = userpath + "/output/rawdata/transmembrane"
    shell_script = settings.ANALYSIS + "transmembrane/run.sh"
    script_arguments = [inputpath, outputpath, outputpathdir]
    annotation_job_id = -1
    for task in taskdetail_dict["task_que"]:
        if task["module"] == 'annotation':
            annotation_job_id = int(task["job_id"])

    if annotation_job_id != -1:
        job_id = slurm_api.submit_job(
            shell_script, script_arguments=script_arguments, dependency_job_ids=[annotation_job_id])
        status = slurm_api.get_job_status(job_id)
        taskdetail_dict = update_task_que(
            taskdetail_dict, "transmembrane", status, job_id)
    else:
        taskdetail_dict["task_status"] = "error"
    return taskdetail_dict


def run_arvf(taskdetail_dict):
    userpath = taskdetail_dict["userpath"]
    inputpath = userpath + "/output/rawdata/annotation/gene.faa"
    outputpath = userpath + "/output/rawdata/arvf"
    shell_script = settings.ANALYSIS + "arvf/run.sh"
    script_arguments = [inputpath, outputpath]
    annotation_job_id = -1
    for task in taskdetail_dict["task_que"]:
        if task["module"] == 'annotation':
            annotation_job_id = int(task["job_id"])

    if annotation_job_id != -1:
        job_id = slurm_api.submit_job(
            shell_script, script_arguments=script_arguments, dependency_job_ids=[annotation_job_id])
        status = slurm_api.get_job_status(job_id)
        taskdetail_dict = update_task_que(
            taskdetail_dict, "arvf", status, job_id)
    else:
        taskdetail_dict["task_status"] = "error"
    return taskdetail_dict

def run_trna(taskdetail_dict):
    userpath = taskdetail_dict["userpath"]
    inputpath = userpath + "/upload/sequence.fasta"
    outputpath = userpath + "/output/rawdata/trna"
    # shell_script = settings.ANALYSIS + "tRNA2/run.sh"
    script_arguments = [inputpath, outputpath]
    shell_script = "/home/platform/phage_db/phage_api/workspace/analysis_script/tRNA2/run.sh"
    job_id = slurm_api.submit_job(
        shell_script, script_arguments=script_arguments)
    status = slurm_api.get_job_status(job_id)
    taskdetail_dict = update_task_que(
        taskdetail_dict, "trna", status, job_id)
    return taskdetail_dict



# /home/platform/phage_db/phage_api/workspace/analysis_script/sequencecomparison/run.sh
# /home/platform/phage_db/phage_api/workspace/analysis_script/sequencecomparison/test/gene.faa
# None
# /home/platform/phage_db/phage_api/workspace/analysis_script/sequencecomparison/test/sequence.gff3
# /home/platform/phage_db/phage_api/workspace/user_task/comparison
# 1
def run_alignment(taskdetail_dict):
    userpath = taskdetail_dict["userpath"]
    inputfaapath = userpath + "/output/rawdata/annotation/gene.faa"
    inputgffpath = userpath + "/output/rawdata/annotation/sequence.gff3"
    outputpathdir = userpath + "/output/rawdata/alignment"
    shell_script = settings.ANALYSIS + "alignment/run.sh"
    script_arguments = [inputfaapath, 'None',inputgffpath, outputpathdir, '1']
    annotation_job_id = -1
    for task in taskdetail_dict["task_que"]:
        if task["module"] == 'annotation':
            annotation_job_id = int(task["job_id"])

    if annotation_job_id != -1:
        job_id = slurm_api.submit_job(
            shell_script, script_arguments=script_arguments, dependency_job_ids=[annotation_job_id])
        status = slurm_api.get_job_status(job_id)
        taskdetail_dict = update_task_que(
            taskdetail_dict, "alignment", status, job_id)
    else:
        taskdetail_dict["task_status"] = "error"
    return taskdetail_dict


# /home/platform/phage_db/phage_api/workspace/analysis_script/terminator/run.sh

# /home/platform/phage_db/phage_api/workspace/user_task/1690265364_4345/output/rawdata/annotation/acc_list.txt

# /home/platform/phage_db/phage_api/workspace/user_task/1690265364_4345/upload/sequence.fasta

# /home/platform/phage_db/phage_api/workspace/user_task/terminator
def run_terminator(taskdetail_dict):
    userpath = taskdetail_dict["userpath"]
    inputacclistpath = userpath + "/output/rawdata/annotation/acc_list.txt"
    inputpath = userpath + "/upload/sequence.fasta"
    outputpathdir = userpath + "/output/rawdata/terminator"
    shell_script = settings.ANALYSIS + "terminator/run.sh"
    script_arguments = [inputacclistpath, inputpath, outputpathdir]
    annotation_job_id = -1
    for task in taskdetail_dict["task_que"]:
        if task["module"] == 'annotation':
            annotation_job_id = int(task["job_id"])

    if annotation_job_id != -1:
        job_id = slurm_api.submit_job(
            shell_script, script_arguments=script_arguments, dependency_job_ids=[annotation_job_id])
        status = slurm_api.get_job_status(job_id)
        taskdetail_dict = update_task_que(
            taskdetail_dict, "terminator", status, job_id)
    else:
        taskdetail_dict["task_status"] = "error"
    return taskdetail_dict



def run_anticrispr(taskdetail_dict):
    userpath = taskdetail_dict["userpath"]

    inputpath = userpath + "/output/rawdata/annotation/gene.faa"
    outputpathdir = userpath + "/output/rawdata/anticrispr"
    shell_script = settings.ANALYSIS + "anticrispr2/run.sh"
    script_arguments = [inputpath, outputpathdir]
    # job_id = slurm_api.submit_job(
    #     shell_script, script_arguments=script_arguments)
    # status = slurm_api.get_job_status(job_id)
    # taskdetail_dict = update_task_que(
    #     taskdetail_dict, "anticrispr", status, job_id)
    
    annotation_job_id = -1
    for task in taskdetail_dict["task_que"]:
        if task["module"] == 'annotation':
            annotation_job_id = int(task["job_id"])

    if annotation_job_id != -1:
        job_id = slurm_api.submit_job(
            shell_script, script_arguments=script_arguments, dependency_job_ids=[annotation_job_id])
        status = slurm_api.get_job_status(job_id)
        taskdetail_dict = update_task_que(
            taskdetail_dict, "anticrispr", status, job_id)
    else:
        taskdetail_dict["task_status"] = "error"
    return taskdetail_dict

def run_crispr(taskdetail_dict):
    userpath = taskdetail_dict["userpath"]

    inputpath = userpath + "/upload/sequence.fasta"
    outputpathdir = userpath + "/output/rawdata/crispr"
    shell_script = settings.ANALYSIS + "crispr/run.sh"
    script_arguments = [inputpath, outputpathdir]
    job_id = slurm_api.submit_job(
        shell_script, script_arguments=script_arguments)
    status = slurm_api.get_job_status(job_id)
    taskdetail_dict = update_task_que(
        taskdetail_dict, "crispr", status, job_id)
    return taskdetail_dict


def run_taxonomic(taskdetail_dict):
    userpath = taskdetail_dict["userpath"]
    inputfaapath = userpath + "/output/rawdata/annotation/gene.faa"
    inputgffpath = userpath + "/output/rawdata/annotation/sequence.gff3"
    outputpathdir = userpath + "/output/rawdata/taxonomic"
    shell_script = settings.ANALYSIS + "taxonomic/run.sh"
    script_arguments = [inputfaapath,inputgffpath, outputpathdir]
    annotation_job_id = -1
    for task in taskdetail_dict["task_que"]:
        if task["module"] == 'annotation':
            annotation_job_id = int(task["job_id"])

    if annotation_job_id != -1:
        job_id = slurm_api.submit_job(
            shell_script, script_arguments=script_arguments, dependency_job_ids=[annotation_job_id])
        status = slurm_api.get_job_status(job_id)
        taskdetail_dict = update_task_que(
            taskdetail_dict, "taxonomic", status, job_id)
    else:
        taskdetail_dict["task_status"] = "error"
    return taskdetail_dict


def run_annotation_pipline(taskdetail_dict):
    module_list = taskdetail_dict["modulelist"]
    for module in module_list:
        if module == "annotation":
            taskdetail_dict = run_annotation(taskdetail_dict)
        elif module == "quality":
            taskdetail_dict = run_quality(taskdetail_dict)
        elif module == "host":
            taskdetail_dict = run_host(taskdetail_dict)
        elif module == "lifestyle":
            taskdetail_dict = run_lifestyle(taskdetail_dict)
        elif module == "trna":
            taskdetail_dict = run_trna(taskdetail_dict)
        elif module == "transmembrane":
            taskdetail_dict = run_transmembrane(taskdetail_dict)
        elif module == "alignment":
            taskdetail_dict = run_alignment(taskdetail_dict)
        elif module == "terminator":
            taskdetail_dict = run_terminator(taskdetail_dict)
        elif module == "crispr":
            taskdetail_dict = run_crispr(taskdetail_dict)
        elif module == "anticrispr":
            taskdetail_dict = run_anticrispr(taskdetail_dict)
        elif module == "arvf":
            taskdetail_dict = run_arvf(taskdetail_dict)
        elif module == "taxonomic":
            taskdetail_dict = run_taxonomic(taskdetail_dict)
    return taskdetail_dict










def run_cluster(taskdetail_dict):
    userpath = taskdetail_dict["userpath"]
    inputpath = userpath + "/upload/sequence.fasta"
    outputpath = userpath + "/output/rawdata/cluster"
    outputpath_tree= userpath + "/output/rawdata/tree"
    outputpath_annotation= userpath + "/output/rawdata/annotation"
    outputpath_alignment= userpath + "/output/rawdata/alignment"
    script_arguments = [inputpath, outputpath,outputpath_tree,outputpath_annotation,outputpath_alignment]
    
    shell_script = "/home/platform/phage_db/phage_api/workspace/analysis_script/clustering/run.sh"

    annotation_job_id = -1
    for task in taskdetail_dict["task_que"]:
        if task["module"] == 'annotation':
            annotation_job_id = int(task["job_id"])

    if annotation_job_id != -1:
        job_id = slurm_api.submit_job(
            shell_script, script_arguments=script_arguments, dependency_job_ids=[annotation_job_id])
        status = slurm_api.get_job_status(job_id)
        taskdetail_dict = update_task_que(
            taskdetail_dict, "cluster", status, job_id)
    else:
        taskdetail_dict["task_status"] = "error"
    return taskdetail_dict



def run_tree(taskdetail_dict):
    userpath = taskdetail_dict["userpath"]
    inputpath = userpath + "/upload/sequence.fasta"
    outputpath_tree= userpath + "/output/rawdata/tree"
    script_arguments = [inputpath,outputpath_tree]

    shell_script = "/home/platform/phage_db/phage_api/workspace/analysis_script/phylogenetictree/run.sh"
    job_id = slurm_api.submit_job(
        shell_script, script_arguments=script_arguments)
    status = slurm_api.get_job_status(job_id)
    taskdetail_dict = update_task_que(
        taskdetail_dict, "tree", status, job_id)
    return taskdetail_dict

def run_cluster_pipline(taskdetail_dict):
    module_list = taskdetail_dict["modulelist"]
    for module in module_list:
        if module == "annotation":
            taskdetail_dict = run_annotation(taskdetail_dict)
        elif module == "cluster":
            taskdetail_dict = run_cluster(taskdetail_dict)
        elif module == "tree":
            taskdetail_dict = run_tree(taskdetail_dict)
        elif module == "alignment":
            taskdetail_dict = run_alignment(taskdetail_dict)
    return taskdetail_dict


