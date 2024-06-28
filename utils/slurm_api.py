import time
import subprocess
from slurmpy import Slurm
from plasmid_api import settings
import re
import sys
# statuslist = ['PENDING', 'RUNNING', 'SUSPENDED', 'COMPLETING', 'COMPLETED',
#               'CANCELLED', 'FAILED', 'TIMEOUT', 'NODE_FAIL', 'PREEMPTED', 'BOOT_FAIL']


def get_job_output(job_id):
    path = settings.TASKLOG + \
        'output/output_'+str(job_id)+'.output'
    try:
        with open(path, 'r') as f:
            output = f.read()
            return output
    except:
        return ''


def get_job_error(job_id):
    path = settings.TASKLOG+'error/error_'+str(job_id)+'.error'
    try:
        with open(path, 'r') as f:
            output = f.read()
            return output
    except:
        return ''


def get_job_status(job_id):
    squeue_command = ["squeue", "--job", str(job_id), "--format=%T"]
    try:
        squeue_output = subprocess.check_output(squeue_command).decode("utf-8")
        lines = squeue_output.strip().split("\n")
        if len(lines) > 1:
            return lines[1].strip()
    except subprocess.CalledProcessError as e:
        print("squeue check error:", e, file=sys.stderr)
        pass

    sacct_command = ["sacct", "--jobs",
                     str(job_id), "--format=JobID,State"]
    try:
        print(sacct_command)
        sacct_output = subprocess.check_output(sacct_command).decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("sacct check error:", e, file=sys.stderr)
        return None
    lines = sacct_output.strip().split("\n")
    for line in lines[1:]:
        parts = line.strip().split()
        if len(parts) == 2 and parts[0] == str(job_id):
            return parts[1]
    return None


def submit_job(shell_script, script_arguments=None, dependency_job_ids=None):
    sbatch_command = ["sbatch"]
    if dependency_job_ids is not None:
        dependencies_str = ":".join(str(job_id)
                                    for job_id in dependency_job_ids)
        sbatch_command.extend(
            ["--dependency=afterok:{}".format(dependencies_str)])
    sbatch_command.append(shell_script)
    if script_arguments is not None:
        sbatch_command.extend(script_arguments)
    sbatch_output = subprocess.check_output(sbatch_command).decode("utf-8")
    job_id = re.search(r"Submitted batch job (\d+)", sbatch_output).group(1)
    return job_id


# script_arguments = ["/home/platform/phage_db/phage_api/workspace/user_task/sequence.fasta",
#                     "/home/platform/phage_db/phage_api/workspace/user_task/1687937755_3180/output"]
# shell_script = "/home/platform/phage_db/phage_api/workspace/analysis_script/annotation/run.sh"

# script_arguments2 = ["/home/platform/phage_db/phage_api/workspace/user_task/1687937755_3180/output/gene.faa",
#                      "/home/platform/phage_db/phage_api/workspace/user_task/1687937755_3180/transoutput"]

# shell_script2 = "/home/platform/phage_db/phage_api/workspace/analysis_script/transmembrane/run.sh"

# job_id = submit_job(shell_script, script_arguments)
# job_id2 = submit_job(shell_script2, script_arguments2, [job_id])

# status = get_job_status(job_id2)

# while status != 'COMPLETED':
#     time.sleep(0.7)
#     status = get_job_status(job_id2)
#     print(status)
#     print(get_job_status(job_id))
