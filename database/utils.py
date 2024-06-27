import os
import requests

def root_path():
    return os.path.dirname(os.path.abspath(__file__))

def esm_fold_api(sequence, pdb_file):
    api_url = 'https://api.esmatlas.com/foldSequence/v1/pdb/'
    x = requests.post(api_url, data = sequence[:399], verify=False)
    with open(pdb_file, 'w') as output:
        print(x.text)
        output.write(x.text)