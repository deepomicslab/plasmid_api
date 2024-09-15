# cat ../../*/data/*.plasmid_list.xls > ALL.plasmid_list.xls
# cat ../../*/data/*.ARG_list.xls > ALL.ARG_list.xls
# cat ../../*/data/*.CRISPR-Cas_list.xls > ALL.CRISPR-Cas_list.xls
# cat ../../*/data/*.protein_list.xls > ALL.protein_list.xls
# cat ../../*/data/*.SMs_list.xls > ALL.SMs_list.xls
# cat ../../*/data/*.SP_list.xls > ALL.SP_list.xls
# cat ../../*/data/*.TMHs_list.xls > ALL.TMHs_list.xls
# cat ../../*/data/*.trna_list.xls > ALL.trna_list.xls
# cat ../../*/data/*.VF_list.xls > ALL.VF_list.xls
import pandas as pd
from database.models import *
sources = {
    'PLSDB': 0,
    'IMG-PR': 1,
    'COMPASS': 2,
    'GenBank': 3,
    'RefSeq': 4,
    'EMBL': 5,
    'Kraken2': 6,
    'DDBJ': 7,
    'TPA': 8,
    'mMGEs': 9
}
data = pd.read_csv('media/data/ALL/data/ALL.plasmid_list.xls', sep='\t')
plasmid_list = []
for index, row in data.iterrows():
    plasmid_list.append(AllPlasmid(plasmid_id=row[0], source=sources[row[1]], topology=row[2], completeness=row[3], length=int(row[4]), gc_content = float(row[5]), host = row[6], mob_type = row[7], mobility = row[8], cluster = row[9], subcluster = row[10], unique_id=row[11]))
AllPlasmid.objects.bulk_create(plasmid_list, batch_size=1000000)