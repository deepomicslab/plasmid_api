from Bio import SeqIO
import os
import pandas as pd
import random

# raw output Data processing

def qualitydetail(taskpath, phageid):
    result = {}
    quality_path = taskpath+'/output/rawdata/quality/quality_summary.tsv'
    qualitys = pd.read_csv(quality_path, sep='\t', index_col=False)
    quality = qualitys[qualitys['contig_id'] == phageid].astype(str)
    result['quality'] = quality.to_dict(orient='records')
    completeness_path = taskpath+'/output/rawdata/quality/completeness.tsv'
    completenesss = pd.read_csv(completeness_path, sep='\t', index_col=False)
    completeness = completenesss[completenesss['contig_id'] == phageid].astype(
        str)

    result['completeness'] = completeness.to_dict(orient='records')

    return result


def hostdetail(taskpath, phageid):
    host_path = taskpath+'/output/rawdata/host/host_predict.txt'
    # accesion_id=l[0], host=l[1], host_source=l[2], Species=l[3], Genus=l[4], Family=l[5], Order=l[6], Class=l[7], Phylum=l[8]
    hosts = pd.read_csv(host_path, sep='\t', index_col=False, header=None, names=[
                        'accesion_id', 'host', 'host_source', 'Species', 'Genus', 'Family', 'Order', 'Class', 'Phylum'])
    host = hosts[hosts['accesion_id'] == phageid]
    return host.to_dict(orient='records')


def trnadetail(taskpath, phageid):
    trnapath = taskpath+'/output/result/trna.tsv'
    trnas = pd.read_csv(trnapath, sep='\t', index_col=False)
    trna = trnas[trnas['phage_accid'] == phageid]
    result = trna.to_dict(orient='records')
    return result


def phageanticrisprdetail(taskpath, phageid):
    anticrisprpath = taskpath+'/output/result/anticrispr.tsv'
    anticrisprs = pd.read_csv(anticrisprpath, sep='\t',
                              index_col=False)
    anticrispr = anticrisprs[anticrisprs['Phage_Acession_ID'] == phageid]
    result = anticrispr.to_dict(orient='records')
    return result


def crisprcasdetail(taskpath, phageid):
    crisprcaspath = taskpath+'/output/rawdata/crisprcas/TSV/Crisprs_REPORT.tsv'
    crisprcass = pd.read_csv(crisprcaspath, sep='\t',
                             index_col=False)
    crisprcas = crisprcass[crisprcass['Sequence'] == phageid]
    result = crisprcas.to_dict(orient='records')
    return result


def transmembranedetail(taskpath, phageid):
    transmembranepath = taskpath+'/output/result/transmembrane.tsv'
    transmembranes = pd.read_csv(transmembranepath, sep='\t', index_col=False)
    transmembrane = transmembranes[transmembranes['phageid'] == phageid].astype(
        str)
    result = transmembrane.to_dict(orient='records')
    return result


def lifestyle(taskpath):
    lifestylepath = taskpath+'/output/rawdata/lifestyle/result.txt'
    lifestyle = pd.read_csv(lifestylepath, sep='\t',
                            index_col=False, names=['phageid', 'lifestyle'])
    result = lifestyle.to_dict(orient='records')
    return result


def host(taskpath):
    hostpath = taskpath+'/output/rawdata/host/host_predict.txt'
    host = pd.read_csv(hostpath, sep='\t',
                       index_col=False, names=[
                           'accesion_id', 'host', 'host_source', 'Species', 'Genus', 'Family', 'Order', 'Class', 'Phylum'])
    result = host.to_dict(orient='records')
    return result


def transmembrane(taskpath):
    # /home/platform/phage_db/phage_api/workspace/user_task/1688724018_2984/output/result/transmembrane.tsv
    transmembranepath = taskpath+'/output/result/transmembrane.tsv'
    transmembranes = pd.read_csv(transmembranepath, sep='\t', index_col=False).astype(
        str)
    result = transmembranes.to_dict(orient='records')
    return result


def cluster(taskpath):
    # /home/platform/phage_db/phage_api/workspace/user_task/1688724018_2984/output/result/transmembrane.tsv
    clusterpath = taskpath+'/output/rawdata/cluster/result.txt'
    clusters = pd.read_csv(clusterpath, sep='\t', index_col=False,names=[
                        'phage_id', 'cluster','subcluster']).astype(
        str)
    clusterslist = clusters.to_dict(orient='records')
    countlist=[]
    for row in clusterslist:
        coutdict={}
        coutdict['phage_id']=row['phage_id']
        #countlist=[{'phage_id':'TemPhD_cluster_55397','hypothetical':0,'infection':3,'assembly':0,'replication':0,'packaging':0,'lysis':0,'regulation':0,'immune':0,'integration':0,'tRNA':0}]
        coutdict['lysis']=random.randint(0, 10)
        coutdict['integration']=random.randint(0, 10)
        coutdict['replication']=random.randint(0, 10)
        coutdict['tRNARelated']=random.randint(0, 10)
        coutdict['regulation']=random.randint(0, 10)
        coutdict['packaging']=random.randint(0, 10)
        coutdict['assembly']=random.randint(0, 10)
        coutdict['infection']=random.randint(0, 10)
        coutdict['immune']=random.randint(0, 10)
        coutdict['hypothetical']=random.randint(0, 10)
        countlist.append(coutdict)
    result = {'cluster':clusterslist,'count':countlist}
    return result

def trna(taskpath):
    trnapath = taskpath+'/output/result/trna.tsv'
    trnas = pd.read_csv(trnapath, sep='\t', index_col=False).astype(
        str)
    result = trnas.to_dict(orient='records')
    return result

def arvgdetail(taskpath):
    arvg_argpath = taskpath+'/output/rawdata/arvf/antimicrobial_resistance_gene_result/antimicrobial_resistance_gene_results.tsv'
    def split_and_join(protein_id):
        return '_'.join(protein_id.split('_')[:-1])
    arvg_arg = pd.read_csv(arvg_argpath, sep='\t', index_col=False,names=[
                        'Protein_id', 'Aligned Protein in CARD']).astype(str)
    arvg_arg['Phage_id'] = arvg_arg['Protein_id'].apply(split_and_join)
    arvg_vfrpath = taskpath+'/output/rawdata/arvf/virulence_factor_result/virulent_factor_results.tsv'
    arvg_vfr = pd.read_csv(arvg_vfrpath, sep='\t', index_col=False,names=[
                        'Protein_id', 'Aligned Protein in VFDB']).astype(str)
    arvg_vfr['Phage_id'] = arvg_vfr['Protein_id'].apply(split_and_join)
    arvg_vfr = arvg_vfr.to_dict(orient='records')
    arvg_arg = arvg_arg.to_dict(orient='records')
    result = {'arvg_arg':arvg_arg,'arvg_vfr':arvg_vfr}
    return result


def taxonomicdetail(taskpath):
    taxnonomicpath = taskpath+'/output/rawdata/taxonomic/tax_result.txt'
    taxonomics = pd.read_csv(taxnonomicpath, sep='\t', index_col=False,names=['phage_id','Predicted_Taxonomy','Number_of_HMM_Hits','Percentage_of_Hits_to_the_Predicted_Taxonomy'])
    taxonomics['Percentage_of_Hits_to_the_Predicted_Taxonomy']=taxonomics['Percentage_of_Hits_to_the_Predicted_Taxonomy'].round(3)
    result=taxonomics.astype(str).to_dict(orient='records')
    return result

def alignmentdetail(taskpath,cid=None,pids=None):
    if cid == None:
        sortedlistpath = taskpath+'/output/rawdata/alignment/phage_list_sort.txt'
        aligncirclepath = taskpath+'/output/rawdata/alignment/comparison_link_circle.csv'
    else:
        sortedlistpath = taskpath+f'/output/rawdata/alignment/{cid}/phage_list_sort.txt'
        aligncirclepath = taskpath+f'/output/rawdata/alignment/{cid}/comparison_link_circle.csv'
    proteinspath = taskpath+'/output/result/protein.tsv'
    originpath = taskpath+'/output/rawdata/annotation/emapper_out.emapper.annotations'
    proteins = pd.read_csv(proteinspath, sep='\t', index_col=False)
    sortedlist=[]
    order=1
    with open(sortedlistpath, 'r') as f:
        sortedlistlines = f.readlines()
        for line in sortedlistlines:
            sortedlist.append({'order':order,'phage_id':line.strip()})
            order+=1
    circlealignments=pd.read_csv(aligncirclepath, sep=',', index_col=False,nrows=30000,names=['id','Source_Phage_ID','Target_Phage_ID',
                                                                            'Source_start_point','Source_end_point','Source_strand',
                                                                            'Source_protein_id','Target_start_point','Target_end_point',
                                                                            'Target_strand','Target_protein_id','Identity','Coverage'                                                     
                                                                            ]).astype(str)
    if pids != None:
        circlealignments=circlealignments[circlealignments['Source_Phage_ID'].isin(pids)]
        circlealignments=circlealignments[circlealignments['Target_Phage_ID'].isin(pids)]
        proteins=proteins[proteins['phageid'].isin(pids)]
    else:
        sortedpid = [sorteddict['phage_id'] for sorteddict in sortedlist]
        pids=sortedpid[:3]
        circlealignments=circlealignments[circlealignments['Source_Phage_ID'].isin(pids)]
        circlealignments=circlealignments[circlealignments['Target_Phage_ID'].isin(pids)]
        proteins=proteins[proteins['phageid'].isin(pids)]
    proteindict = proteins.to_dict(orient='records')
    newdict = []
    data = pd.read_csv(originpath, header=None, sep='\t', comment='#')
    # data = data[data[0].str.contains(phageid)]

    for item in proteindict:
        cog_category = list(data[data[0] == item["Protein_id"]][6])
        if len(cog_category):
            cog_category = cog_category[0]
        else:
            cog_category = 'S'
        if cog_category == '-':
            cog_category = 'S'
        new_item = {
            "protein_id": item["Protein_id"],
            "plasmid_id": item["phageid"],
            "product": item["Protein_product"],
            "cog_category": cog_category,
            "protein_function_prediction_source": item['protein_function_prediction_source'],
            "start": item['Start_location'],
            "end": item['Stop_location'],
            "strand": item['Strand'],
            "sequence": item['sequence'],
        }
        newdict.append(item|new_item)
    result ={
            'sortedlist':sortedlist,
            'circlealignment':circlealignments.to_dict(orient='records'),
            'proteins':newdict
            }
    return result

def terminatordetail(taskpath):
    #/home/platform/phage_db/phage_api/workspace/user_task/1690380527_6812/output/rawdata/terminator/transterm_output.txt
    terminatorspath = taskpath+'/output/rawdata/terminator/transterm_output.txt'
    terminators = pd.read_csv(terminatorspath, sep='\t', index_col=False,names=['Phage_id','Terminator_Id','Start','Stop','Sense','Loc','Confidence']).astype(str)
    result = terminators.to_dict(orient='records')
    return result


def crisprdetail(taskpath):
    #/home/platform/phage_db/phage_api/workspace/user_task/1690814265_3361/output/rawdata/crispr/output/TSV/Crisprs_REPORT.tsv
    crisprpath = taskpath+'/output/rawdata/crispr/output/TSV/Crisprs_REPORT.tsv'
    #Strain	Sequence	Sequence_basename	Duplicated_Spacers	CRISPR_Id	CRISPR_Start	CRISPR_End	CRISPR_Length	Potential_Orientation (AT%)	CRISPRDirection	Consensus_Repeat	Repeat_ID (CRISPRdb)	Nb_CRISPRs_with_same_Repeat (CRISPRdb)	Repeat_Length	Spacers_Nb	Mean_size_Spacers	Standard_Deviation_Spacers	Nb_Repeats_matching_Consensus	Ratio_Repeats_match/TotalRepeat	Conservation_Repeats (% identity)	EBcons_Repeats	Conservation_Spacers (% identity)	EBcons_Spacers	Repeat_Length_plus_mean_size_Spacers	Ratio_Repeat/mean_Spacers_Length	CRISPR_found_in_DB (if sequence IDs are similar)	Evidence_Level
    crisprs= pd.read_csv(crisprpath, sep='\t', index_col=False).astype(str)
    result = crisprs.to_dict(orient='records')
    
    return result


def anticrisprdetail(taskpath):
    anticrisprpath = taskpath+'/output/result/anticrispr.tsv'
    anticrisprs = pd.read_csv(anticrisprpath, sep='\t',
                            index_col=False).astype(str)
    result = anticrisprs.to_dict(orient='records')
    return result