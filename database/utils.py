import os
import requests

def root_path():
    return os.path.dirname(os.path.abspath(__file__))

def esm_fold_api(sequence, pdb_file):
    api_url = 'https://api.esmatlas.com/foldSequence/v1/pdb/'
    sequence = sequence[:390]
    print(len(sequence))
    x = requests.post(api_url, data = sequence, verify=False)
    with open(pdb_file, 'w') as output:
        print(x.text)
        output.write(x.text)