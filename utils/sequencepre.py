from Bio import SeqIO
import os
import csv
import pandas as pd
import re


def phageFastaToCSV(userpath):
    fatsapath = userpath+'/upload/sequence.fasta'
    outputpath = userpath+'/output/result/'
    header = '\t'.join(['Acession_ID', 'gc_content', 'length'])
    lines = [header]
    with open(fatsapath, 'r') as fasfile:
        for record in SeqIO.parse(fasfile, 'fasta'):
            phagepath = outputpath+record.id
            os.makedirs(phagepath, exist_ok=False)
            with open(phagepath+'/sequence.fasta', 'w') as seqfile:
                seqfile.write('>'+record.id+'\n'+str(record.seq))
            gc_count = record.seq.count("G") + record.seq.count("C")
            gc_content = gc_count / len(record.seq) * 100
            line = [record.id, str(gc_content), str(len(record.seq))]
            lines.append('\t'.join(line))
    csvpath = outputpath+'phage.tsv'
    with open(csvpath, 'w') as csvfile:
        csvfile.write('\n'.join(lines))


def proteindata(userpath):
    annpath = userpath+'/output/rawdata/annotation'
    outputpath = userpath+'/output/result/'
    phagepath = outputpath+'/phage.tsv'
    phageids = []
    with open(phagepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            phageids.append(dict(row)['Acession_ID'])
    accpath = annpath+'/acc_list.txt'
    faapath = annpath+'/gene.faa'
    lines = []
    proteindict = {}
    with open(accpath, 'r') as accfile:
        acclines = accfile.readlines()
        for accline in acclines:
            acclist = accline.strip().split('	')
            proteinid = acclist[0]
            # find phageid
            for phageid in phageids:
                if phageid in proteinid:
                    proteindict[proteinid] = [phageid, acclist[1], acclist[6], acclist[2]]
    with open(faapath, 'r') as faafile:
        for record in SeqIO.parse(faafile, 'fasta'):
            proteinInfo = record.description.split(' # ')
            proteindict[record.id].append(proteinInfo[1])
            proteindict[record.id].append(proteinInfo[2])
            if proteinInfo[3] == '1':
                proteindict[record.id].append('+')
            else:
                proteindict[record.id].append('-')
            proteindict[record.id].append(str(record.seq))
    proteincsvpath = outputpath+'/protein.tsv'
    header = '\t'.join(['Protein_id', 'phageid', 'Protein_product',
                        'Protein_function_classification', 'protein_function_prediction_source','Start_location', 'Stop_location', 'Strand', 'sequence'])
    with open(proteincsvpath, 'w') as csvfile:
        csvfile.write(header+'\n')
        for proteinid in proteindict.keys():
            line = [proteinid]
            line.extend(proteindict[proteinid])
            lines.append('\t'.join(line))
        csvfile.write('\n'.join(lines))


def upadtephagecsv_genes(userpath):
    outputpath = userpath+'/output/result/'
    phagepath = outputpath+'/phage.tsv'
    proteincsvpath = outputpath+'/protein.tsv'
    phage = pd.read_csv(phagepath, sep='\t')
    protein = pd.read_csv(proteincsvpath, sep='\t')
    countdict = protein['phageid'].value_counts().to_dict()
    phage['genes'] = phage['Acession_ID'].map(countdict)
    phage.to_csv(phagepath, sep='\t', index=False)


def upadtephagecsv_checkv(userpath):
    outputpath = userpath+'/output/'
    checkvresult = outputpath+'rawdata/quality/checkv_result.txt'
    phagepath = outputpath+'result/phage.tsv'
    phage = pd.read_csv(phagepath, sep='\t', index_col=False)
    checkv = pd.read_csv(checkvresult, sep='\t', header=None)
    checkv.columns = ['Acession_ID', 'completeness', 'taxonomy']

    def addcompleteness(row):
        return checkv[checkv['Acession_ID'] == row['Acession_ID']].completeness.values[0]
    phage['completeness'] = phage.apply(addcompleteness, axis=1)
    phage.to_csv(phagepath, sep='\t', index=False)


def updatephagecsv_host(userpath):
    outputpath = userpath+'/output/'
    host = outputpath+'rawdata/host/host_predict.txt'
    phagepath = outputpath+'result/phage.tsv'
    phage = pd.read_csv(phagepath, sep='\t', index_col=False)
    host = pd.read_csv(host, sep='\t', header=None, index_col=False)

    def addhost(row):
        return host[host[0] == row['Acession_ID']][1].values[0]
    phage['host'] = phage.apply(addhost, axis=1)
    phage.to_csv(phagepath, sep='\t', index=False)


def updatephagecsv_lifestyle(userpath):
    outputpath = userpath+'/output/'
    lifestyle = outputpath+'rawdata/lifestyle/result.txt'
    phagepath = outputpath+'result/phage.tsv'
    phage = pd.read_csv(phagepath, sep='\t', index_col=False)
    lifestyle = pd.read_csv(lifestyle, sep='\t', header=None, index_col=False)

    def addlifestyle(row):
        return lifestyle[lifestyle[0] == row['Acession_ID']][1].values[0]

    phage['lifestyle'] = phage.apply(addlifestyle, axis=1)
    phage.to_csv(phagepath, sep='\t', index=False)


def updatephagecsv_trna(userpath):
    outputpath = userpath+'/output/'
    trnapath = outputpath+'rawdata/trna/trna.fasta'
    resultpath = outputpath+'result/trna.tsv'
    # trna_id=l[0], trnatype=l[1], start=l[2], end=l[3], strand=l[4], length=l[5], permutation=l[6], seq=l[7], phage_accid=l[8]
    with open(resultpath, 'a') as f:
        f.write(
            "trna_id\tsource\ttrnatype\tstart\tend\tstrand\tlength\tpermutation\tseq\tphage_accid\n")
    with open(trnapath, 'r') as fasfile:
        for record in SeqIO.parse(fasfile, 'fasta'):
            headersplit = record.description.split(" ")
            phageid = '-'.join(record.id.split('-')[:-2])
            source= record.id.split('-')[-1]
            if 'Permuted' in headersplit[2]:
                with open(resultpath, 'a') as f:
                    f.write(headersplit[0]+'\t' +source+'\t'+ headersplit[1]+'\t'+'-'+'\t'+'-'+'\t-\t'+str(
                        len(str(record.seq)))+'\t' + headersplit[2][10:]+'\t' + str(record.seq) + '\t' + phageid+'\n')
            elif headersplit[2].startswith('c'):
                pos = eval(headersplit[2][1:])
                with open(resultpath, 'a') as f:
                    f.write(headersplit[0]+'\t' +source+'\t'+ headersplit[1]+'\t'+str(pos[0])+'\t'+str(
                        pos[1])+'\treverse\t'+str(len(str(record.seq)))+'\t' + '-'+'\t'+str(record.seq) + '\t' + phageid+'\n')
            else:
                pos = eval(headersplit[2])
                with open(resultpath, 'a') as f:
                    f.write(headersplit[0]+'\t' +source+'\t'+ headersplit[1]+'\t'+str(pos[0])+'\t'+str(
                        pos[1])+'\tforward\t'+str(len(str(record.seq)))+'\t' + '-'+'\t' + str(record.seq) + '\t' + phageid+'\n')


def anticrisprprocess(userpath):
    outputpath = userpath+'/output/'
    anticrisprpath = outputpath+'rawdata/anticrispr/acr_result.txt'
    antidict = {}
    with open(anticrisprpath, 'r') as f:
        for line in f.readlines():
            antidict[line.strip().split('\t')[0]] = line.strip().split('\t')[1]

    proteinpath = outputpath+'result/protein.tsv'
    protein = pd.read_csv(proteinpath, sep='\t', index_col=False)
    protein = protein[protein['Protein_id'].isin(antidict.keys())]
    if protein.empty:
        protein.to_csv(outputpath+'result/anticrispr.tsv', sep='\t', index=False)
    else:
        def addantiresource(row):
            return antidict[row['Protein_id']]
        protein['antiresource'] = protein.apply(addantiresource, axis=1)
        protein.to_csv(outputpath+'result/anticrispr.tsv', sep='\t', index=False)
    


def transmembraneproprocess(userpath):
    outputpath = outputpath = userpath+'/output/'
    protein = pd.read_csv(outputpath+'result/protein.tsv',
                          sep='\t', index_col=False)
    protdict = {}
    # phageid    Length  predictedTMHsNumber ExpnumberofAAsinTMHs    Expnumberfirst60AAs TotalprobofNin  POSSIBLENterm   insidesource    insidestart insideend   TMhelixsource   TMhelixstart    TMhelixend  outsidesource   outsidestart    outsideend
    for pro in protein.values:
        newobj = {'Phage_Acession_ID': pro[1], 'Length': '', 'predictedTMHsNumber': '', 'ExpnumberofAAsinTMHs': '', 'Expnumberfirst60AAs': '', 'TotalprobofNin': '', 'POSSIBLENterm': '',
                  'insidesource': '', 'insidestart': '', 'insideend': '', 'TMhelixsource': '', 'TMhelixstart': '', 'TMhelixend': '', 'outsidesource': '', 'outsidestart': '', 'outsideend': ''}
        protdict[pro[0]] = newobj
    with open(outputpath+'/rawdata/transmembrane/result.txt', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('#'):
                obj = protdict[line.split(' ')[1]]
                if 'Length' in line:
                    obj['Length'] = line.split(': ')[1]
                elif 'Number of predicted TMHs' in line:
                    obj['predictedTMHsNumber'] = line.split(':  ')[1]
                elif 'Exp number of AAs in TMHs' in line:
                    obj['ExpnumberofAAsinTMHs'] = line.split(': ')[1]
                elif 'Exp number, first 60 AAs' in line:
                    obj['Expnumberfirst60AAs'] = line.split(':  ')[1]
                elif 'Total prob of N-in' in line:
                    obj['TotalprobofNin'] = line.split(':        ')[1]
                elif 'POSSIBLE N-term signal sequence' in line:
                    obj['POSSIBLENterm'] = True
            else:
                obj = protdict[line.split('	')[0]]
                pattern = r'\d+'
                if 'inside' in line:
                    obj['insidesource'] = line.split('\t')[1]
                    matches = re.findall(pattern, line.split('\t')[3])
                    obj['insidestart'] = matches[0]
                    obj['insideend'] = matches[1]
                elif 'TMhelix' in line:
                    obj['TMhelixsource'] = line.split('\t')[1]
                    matches = re.findall(pattern, line.split('\t')[3])
                    obj['TMhelixstart'] = matches[0]
                    obj['TMhelixend'] = matches[1]
                elif 'outside' in line:
                    obj['outsidesource'] = line.split('\t')[1]
                    matches = re.findall(pattern, line.split('\t')[3])
                    obj['outsidestart'] = matches[0]
                    obj['outsideend'] = matches[1]
    convertlist = []
    for key, value in protdict.items():
        value['Protein_id'] = key
        convertlist.append(value)
    df = pd.DataFrame(convertlist)
    df.to_csv(outputpath+'result/transmembrane.tsv', sep='\t', index=False)


def upadtephagecsv_taxonomy(userpath):
    outputpath = userpath+'/output/'
    #workspace/user_task/1691131533_5204/output/rawdata/taxnonomic/tax_result.txt
    taxresult = outputpath+'rawdata/taxonomic/tax_result.txt'
    phagepath = outputpath+'result/phage.tsv'
    phage = pd.read_csv(phagepath, sep='\t', index_col=False)
    taxonomys = pd.read_csv(taxresult, sep='\t', header=None)
    taxonomys.columns = ['Acession_ID', 'taxonomy', 'protein_num','confidence']

    def addtaxonomy(row):
        return taxonomys[taxonomys['Acession_ID'] == row['Acession_ID']].taxonomy.values[0]
    phage['taxonomy'] = phage.apply(addtaxonomy, axis=1)
    phage.to_csv(phagepath, sep='\t', index=False)

# phagefastapreprocess(
#     '/home/ys/code/phage/Phage_api/user_task/1686563619_9016/upload/', '/home/ys/code/phage/Phage_api/user_task/1686563619_9016/output/result/')
# proteindata('/home/ys/code/phage/Phage_api/user_task/1686563619_9016/output/rawdata/ana/',
#             '/home/ys/code/phage/Phage_api/user_task/1686563619_9016/output/result/')
# upadtephagecsv_checkv(
#     '/home/ys/code/phage/Phage_api/user_task/1686563619_9016/output/')
# updatephagecsv_host(
#     '/home/ys/code/phage/Phage_api/user_task/1686563619_9016/output/')
# updatephagecsv_lifestyle(
#     '/home/ys/code/phage/Phage_api/user_task/1686563619_9016/output/')
# trnaprocess(
#     '/home/ys/code/phage/Phage_api/user_task/1686563619_9016/output/')
# transmembraneproprocess(
    # '/home/ys/code/phage/Phage_api/user_task/1686563619_9016/output/')


# phagefastapreprocess(
#     '/home/platform/phage_db/phage_api/workspace/user_task/1688041831_2432')

# proteindata(
#     '/home/platform/phage_db/phage_api/workspace/user_task/1688041831_2432')
# upadtephagecsv_genes(
#     '/home/platform/phage_db/phage_api/workspace/user_task/1688041831_2432')

# upadtephagecsv_checkv(
#     '/home/platform/phage_db/phage_api/workspace/user_task/1688041831_2432')
# updatephagecsv_host(
#     '/home/platform/phage_db/phage_api/workspace/user_task/1688041831_2432')
# updatephagecsv_lifestyle(
#     '/home/platform/phage_db/phage_api/workspace/user_task/1688041831_2432')


#trnaprocess('/home/platform/phage_db/phage_api/workspace/user_task/1690101565_1426')