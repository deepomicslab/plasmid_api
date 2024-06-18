import pandas as pd
from database.models import *

print('load plasmid list')
data = pd.read_csv('media/data/Kraken2./Kraken2.plasmid_list.xls', sep='\t')
Plasmid.objects.all().delete()
for index, row in data.iterrows():
    Plasmid.objects.create(plasmid_id=row[0], source=1, topology=row[2], completeness=row[3], length=int(row[4]), gc_content = float(row[5]), host = row[6], mob_type = row[7], mobility = row[8], cluster = row[9], subcluster = row[10])

print('load host list')
data = pd.read_csv('media/data/Kraken2./Kraken2.host_list.xls', sep='\t')
Host.objects.all().delete()
for index, row in data.iterrows():
    plasmid_id=row[0]
    plasmid = Plasmid.objects.get(plasmid_id=plasmid_id)
    Host.objects.create(plasmid=plasmid, name=row[1], species=row[3], genus=row[4], family=row[5], order = row[6], host_class = row[7], phylum = row[8])

print('load trna list')
data = pd.read_csv('media/data/Kraken2./Kraken2.trna_list.xls', sep='\t')
tRNA.objects.all().delete()
for index, row in data.iterrows():
    plasmid_id=row[0]
    plasmid = Plasmid.objects.get(plasmid_id=plasmid_id)
    if row[5] == 'forward':
        strand = 0
    else:
        strand = 1
    tRNA.objects.create(plasmid=plasmid, trna_id=row[1], trna_type=row[2], start=int(row[3]), end=int(row[4]), strand=strand, length = int(row[6]), sequence = row[7])

print('load protein list')
data = pd.read_csv('media/data/Kraken2./Kraken2.protein_list.xls', sep='\t')
Protein.objects.all().delete()
for index, row in data.iterrows():
    plasmid_id=row[0]
    plasmid = Plasmid.objects.get(plasmid_id=plasmid_id)
    if row[6] == '+':
        strand = 0
    else:
        strand = 1
    Protein.objects.create(plasmid=plasmid, protein_id=row[1], orf_source=row[3], start=int(row[4]), end=int(row[5]), strand=strand, product = row[7], cog_category=row[8], function_source = row[9], ec_number=row[10], cog_id=row[11], go=row[12], kegg_ko=row[13], kegg_pathway=row[14], kegg_module=row[15], kegg_reaction=row[16], kegg_rclass=row[17], brite=row[18], kegg_tc=row[19], cazy=row[20], bigg_reaction=row[21], pfam=row[22], uni_port_kb=row[23], sequence=row[24])

print('load hostnode list')
for host in Host.objects.values('phylum').distinct():
    phylum = host['phylum']
    if phylum == 'nan': continue
    plasmid_count = Host.objects.filter(phylum=phylum).count()
    HostNode.objects.create(node=phylum, rank='Phylum', plasmid_count=plasmid_count)

    for host_class in Host.objects.filter(phylum=phylum).values('phylum', 'host_class').distinct():
        class_node = host_class['host_class']
        if class_node == 'nan': continue
        plasmid_count = Host.objects.filter(phylum=phylum, host_class=class_node).count()
        HostNode.objects.create(node=class_node, rank='Class', plasmid_count=plasmid_count, parent=phylum)

        for order in Host.objects.filter(phylum=phylum, host_class=class_node).values('phylum', 'host_class', 'order').distinct():
            order_node = order['order']
            if order_node == 'nan': continue
            plasmid_count = Host.objects.filter(phylum=phylum, host_class=class_node, order=order_node).count()
            HostNode.objects.create(node=order_node, rank='Order', plasmid_count=plasmid_count, parent=class_node)

            for family in Host.objects.filter(phylum=phylum, host_class=class_node, order=order_node).values('phylum', 'host_class', 'order', 'family').distinct():
                family_node = family['family']
                if family_node == 'nan': continue
                plasmid_count = Host.objects.filter(phylum=phylum, host_class=class_node, order=order_node, family=family_node).count()
                HostNode.objects.create(node=family_node, rank='Family', plasmid_count=plasmid_count, parent=order_node)

                for genus in Host.objects.filter(phylum=phylum, host_class=class_node, order=order_node, family=family_node).values('phylum', 'host_class', 'order', 'family', 'genus').distinct():
                    genus_node = genus['genus']
                    if genus_node == 'nan': continue
                    plasmid_count = Host.objects.filter(phylum=phylum, host_class=class_node, order=order_node, family=family_node, genus=genus_node).count()
                    HostNode.objects.create(node=genus_node, rank='Genus', plasmid_count=plasmid_count, parent=family_node)

                    for species in Host.objects.filter(phylum=phylum, host_class=class_node, order=order_node, family=family_node, genus=genus_node).values('phylum', 'host_class', 'order', 'family', 'genus', 'species').distinct():
                        species_node = species['species']
                        if species_node == 'nan': continue
                        plasmid_count = Host.objects.filter(phylum=phylum, host_class=class_node, order=order_node, family=family_node, genus=genus_node, species=species_node).count()
                        HostNode.objects.create(node=species_node, rank='Species', plasmid_count=plasmid_count, parent=genus_node)

print('load args list')
data = pd.read_csv('media/data/Kraken2./Kraken2.ARG_list.xls', sep='\t')
AntimicrobialResistanceGene.objects.all().delete()
for index, row in data.iterrows():
    if index > 10000:
        break
    plasmid_id=row[0]
    plasmid = Plasmid.objects.get(plasmid_id=plasmid_id)
    if row[5] == '+':
        strand = 0
    else:
        strand = 1
    AntimicrobialResistanceGene.objects.create(plasmid=plasmid, protein_id=row[1], orf_source=row[2], start=int(row[3]), end=int(row[4]), strand=strand, product = row[6], cutoff = row[7], hsp_identifier=row[8], best_hit_aro=row[9], best_identities=row[10], aro=row[11], drug_class=row[12], resistance_mechanism=row[13], amr_gene_family=row[14], antibiotic=row[15], sequence=row[16], snps_in_best_hit_aro=row[17], other_snps=row[18])

print('load sms list')
data = pd.read_csv('media/data/Kraken2./Kraken2.SMs_list.xls', sep='\t')
SecondaryMetabolism.objects.all().delete()
for index, row in data.iterrows():
    if index > 10000:
        break
    plasmid_id=row[0]
    plasmid = Plasmid.objects.get(plasmid_id=plasmid_id)
    SecondaryMetabolism.objects.create(plasmid=plasmid, region=row[1],start=int(row[2]), end=int(row[3]), type=row[4], most_similar_known_cluster = row[5], similarity = row[6])

print('load sps list')
data = pd.read_csv('media/data/Kraken2./Kraken2.SP_list.xls', sep='\t')
SignalPeptides.objects.all().delete()
for index, row in data.iterrows():
    if index > 10000:
        break
    plasmid_id=row[0]
    plasmid = Plasmid.objects.get(plasmid_id=plasmid_id)
    if row[4] == '+':
        strand = 0
    else:
        strand = 1
    SignalPeptides.objects.create(plasmid=plasmid, protein_id=row[1], start=int(row[2]), end=int(row[3]), strand=strand, product = row[5], prediction = row[6], other=row[7], sp=row[8], lipo=row[9], tat=row[10], tatlipo=row[11], pilin=row[12], cs_position=row[13], probability_of_cs_position=row[14])

print('load tmhs list')
data = pd.read_csv('media/data/Kraken2./Kraken2.TMHs_list.xls', sep='\t')
TransmembraneHelices.objects.all().delete()
Helices.objects.all().delete()
tmh = None
for index, row in data.iterrows():
    if index > 10000:
        break
    plasmid_id=row[0]
    plasmid = Plasmid.objects.get(plasmid_id=plasmid_id)
    if row[4] == '+':
        strand = 0
    else:
        strand = 1

    if tmh == None or int(row[9]) == 1:
        tmh = TransmembraneHelices.objects.create(plasmid=plasmid, protein_id=row[1], start=int(row[2]), end=int(row[3]), strand=strand, length = row[5], number_of_predicted_tmhs = row[6], source=row[7], exp_number_of_aas_in_tmhs=row[11], exp_numberof_first_60_aas=row[12], total_prob_of_n_in=row[13])
        Helices.objects.create(tmh=tmh, position=row[8], self_start=row[9], self_end=row[10])
    else:
        Helices.objects.create(tmh=tmh, position=row[8], self_start=row[9], self_end=row[10])

print('load vfs list')
data = pd.read_csv('media/data/Kraken2./Kraken2.VF_list.xls', sep='\t')
VirulentFactor.objects.all().delete()
for index, row in data.iterrows():
    if index > 10000:
        break
    plasmid_id=row[0]
    plasmid = Plasmid.objects.get(plasmid_id=plasmid_id)
    if row[5] == '+':
        strand = 0
    else:
        strand = 1
    VirulentFactor.objects.create(plasmid=plasmid, protein_id=row[1], orf_source=row[2], start=int(row[3]), end=int(row[4]), strand=strand, vf_seq_id = row[6], identity = row[7], e_value=row[8], gene_name=row[9], product=row[10], vf_id=row[11], vf_name=row[12], vf_fullname=row[13], vf_cid=row[14], vf_category=row[15], characteristics=row[16], structure=row[17], function=row[18], mechanism=row[19], sequence=row[20])

print('load crispr list')
data = pd.read_csv('media/data/Kraken2./Kraken2.CRISPR-Cas_list.xls', sep='\t')
Crispr.objects.all().delete()
for index, row in data.iterrows():
    plasmid_id=row[0]
    plasmid = Plasmid.objects.get(plasmid_id=plasmid_id)
    
    Crispr.objects.create(plasmid=plasmid, cas_id=row[1], cas_start=int(row[2]), cas_end=int(row[3]), cas_subtype=row[4], crispr_id=row[5], start=int(row[6]), end=int(row[7]), crispr_subtype=row[8], cas_consenus_prediction = row[9], consensus_repeat_sequence = row[10], cas_genes=row[11])

print('load cluster list')
data = pd.read_csv('media/data/Kraken2./clusters_list.xls', sep='\t')
Cluster.objects.all().delete()
for index, row in data.iterrows():
    Cluster.objects.create(cluster_id=row[0], avg_gc=float(row[1]), avg_length=float(row[2]), no_of_subclusters=int(row[4]), no_of_members=row[6])

print('load subcluster list')
data = pd.read_csv('media/data/Kraken2./subclusters_list.xls', sep='\t')
Subcluster.objects.all().delete()
for index, row in data.iterrows(): 
    cluster_id =row[5]
    cluster = Cluster.objects.get(cluster_id=cluster_id)
    Subcluster.objects.create(cluster=cluster, subcluster_id=row[0], avg_gc=float(row[1]), avg_length=float(row[2]), no_of_members=row[4], members=row[3])