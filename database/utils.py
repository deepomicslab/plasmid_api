import os
import requests

def root_path():
    return os.path.dirname(os.path.abspath(__file__))

def esm_fold_pdb_api(sequence, pdb_file=None):
    api_url = 'https://api.esmatlas.com/foldSequence/v1/pdb/'
    x = requests.post(api_url, data = sequence[:399], verify=False)
    if pdb_file:
        with open(pdb_file, 'w') as output:
            output.write(x.text)
    else:
        return x.text

def esm_fold_cif_api(sequence, pdb_file=None):
    api_url = 'https://api.esmatlas.com/foldSequence/v1/cif/'
    x = requests.post(api_url, data = sequence[:399], verify=False)
    
    return x.text