from django.db import models

# Create your models here.
class Plasmid(models.Model):
    SOURCE_TYPE = (
        (0, 'PLSDB'),
        (1, 'IMG-PR'),
        (2, 'COMPASS'),
        (3, 'GenBank'),
        (4, 'RefSeq'),
        (5, 'EMBL'),
        (6, 'Kraken2'),
        (7, 'DDBJ'),
        (8, 'TPA'),
    )
    plasmid_id = models.CharField(max_length=200)
    source = models.IntegerField(default=0, choices=SOURCE_TYPE)
    topology = models.CharField(max_length=200, null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    gc_content = models.FloatField(null=True, blank=True)
    host = models.TextField(blank=True, null=True)
    completeness = models.CharField(max_length=200, blank=True, null=True)
    mob_type = models.TextField(blank=True, null=True)
    mobility = models.TextField(blank=True, null=True)
    cluster = models.CharField(max_length=200, blank=True, null=True)
    subcluster = models.CharField(max_length=200, blank=True, null=True)

class Protein(models.Model):
    STRAND = (
        (0, '+'),
        (1, '-'),
    )
    plasmid = models.ForeignKey(Plasmid, on_delete=models.CASCADE, related_name="proteins")
    protein_id = models.CharField(max_length=200)
    orf_source = models.CharField(max_length=200, null=True, blank=True)
    start = models.IntegerField(null=True, blank=True)
    end = models.IntegerField(null=True, blank=True)
    strand = models.IntegerField(default=0, choices=STRAND)
    product = models.CharField(max_length=200, null=True, blank=True)
    function_source = models.CharField(max_length=200, null=True, blank=True)
    cog_category = models.CharField(max_length=200, null=True, blank=True)
    ec_number = models.CharField(max_length=200, null=True, blank=True)
    cog_id = models.CharField(max_length=200, null=True, blank=True)
    go = models.TextField(blank=True, null=True)
    kegg_ko = models.TextField(blank=True, null=True)
    kegg_pathway = models.TextField(blank=True, null=True)
    kegg_module = models.TextField(blank=True, null=True)
    kegg_reaction = models.TextField(blank=True, null=True)
    kegg_rclass = models.TextField(blank=True, null=True)
    brite = models.TextField(blank=True, null=True)
    kegg_tc = models.TextField(blank=True, null=True)
    cazy = models.TextField(blank=True, null=True)
    bigg_reaction = models.TextField(blank=True, null=True)
    pfam = models.TextField(blank=True, null=True)
    uni_port_kb = models.TextField(blank=True, null=True)
    sequence = models.TextField(blank=True, null=True)

class Host(models.Model):
    plasmid = models.ForeignKey(Plasmid, on_delete=models.CASCADE, related_name="hosts")
    name = models.CharField(max_length=200)
    species = models.CharField(max_length=200, null=True, blank=True)
    genus = models.CharField(max_length=200, null=True, blank=True)
    family = models.CharField(max_length=200, null=True, blank=True)
    order = models.CharField(max_length=200, null=True, blank=True)
    host_class = models.CharField(max_length=200, null=True, blank=True)
    phylum = models.CharField(max_length=200, null=True, blank=True)

class HostNode(models.Model):
    node = models.CharField(max_length=200, blank=True, null=True)
    parent = models.CharField(max_length=200, blank=True, null=True)
    rank = models.CharField(max_length=200, blank=True, null=True)
    plasmid_count = models.IntegerField(blank=True, null=True)


class tRNA(models.Model):
    STRAND = (
        (0, 'forward'),
        (1, 'reverse'),
    )
    plasmid = models.ForeignKey(Plasmid, on_delete=models.CASCADE, related_name="trans")
    trna_id = models.CharField(max_length=200)
    trna_type = models.CharField(max_length=200, null=True, blank=True)
    start = models.IntegerField(null=True, blank=True)
    end = models.IntegerField(null=True, blank=True)
    strand = models.IntegerField(default=0, choices=STRAND)
    length = models.IntegerField(null=True, blank=True)
    sequence = models.TextField(blank=True, null=True)

class AntimicrobialResistanceGene(models.Model):
    STRAND = (
        (0, '+'),
        (1, '-'),
    )
    plasmid = models.ForeignKey(Plasmid, on_delete=models.CASCADE, related_name="args")
    protein_id = models.CharField(max_length=200)
    orf_source = models.CharField(max_length=200, null=True, blank=True)
    start = models.IntegerField(null=True, blank=True)
    end = models.IntegerField(null=True, blank=True)
    strand = models.IntegerField(default=0, choices=STRAND)
    product = models.CharField(max_length=200, null=True, blank=True)
    cutoff = models.CharField(max_length=200, null=True, blank=True)
    hsp_identifier = models.CharField(max_length=200, null=True, blank=True)
    best_hit_aro = models.CharField(max_length=200, null=True, blank=True)
    best_identities = models.FloatField(null=True, blank=True)
    aro = models.IntegerField(null=True, blank=True)
    drug_class = models.TextField(blank=True, null=True)
    resistance_mechanism = models.TextField(blank=True, null=True)
    amr_gene_family = models.TextField(blank=True, null=True)
    antibiotic = models.TextField(blank=True, null=True)
    sequence = models.TextField(blank=True, null=True)
    snps_in_best_hit_aro = models.TextField(blank=True, null=True)
    other_snps = models.TextField(blank=True, null=True)
    

class SecondaryMetabolism(models.Model):
    plasmid = models.ForeignKey(Plasmid, on_delete=models.CASCADE, related_name="sms")
    region = models.CharField(max_length=200, null=True, blank=True)
    start = models.IntegerField(null=True, blank=True)
    end = models.IntegerField(null=True, blank=True)
    type = models.TextField(blank=True, null=True)
    most_similar_known_cluster = models.TextField(blank=True, null=True)
    similarity = models.CharField(max_length=200, null=True, blank=True)

class SignalPeptides(models.Model):
    STRAND = (
        (0, '+'),
        (1, '-'),
    )
    plasmid = models.ForeignKey(Plasmid, on_delete=models.CASCADE, related_name="sps")
    protein_id = models.CharField(max_length=200)
    start = models.IntegerField(null=True, blank=True)
    end = models.IntegerField(null=True, blank=True)
    strand = models.IntegerField(default=0, choices=STRAND)
    product = models.CharField(max_length=200, null=True, blank=True)
    prediction = models.CharField(max_length=200, null=True, blank=True)
    other = models.FloatField(null=True, blank=True)
    sp = models.FloatField(null=True, blank=True)
    lipo = models.FloatField(null=True, blank=True)
    tat = models.FloatField(null=True, blank=True)
    tatlipo = models.FloatField(null=True, blank=True)
    pilin = models.FloatField(null=True, blank=True)
    cs_position = models.CharField(max_length=200, null=True, blank=True)
    probability_of_cs_position = models.FloatField(null=True, blank=True)

class TransmembraneHelices(models.Model):
    STRAND = (
        (0, '+'),
        (1, '-'),
    )
    plasmid = models.ForeignKey(Plasmid, on_delete=models.CASCADE, related_name="tmhs")
    protein_id = models.CharField(max_length=200)
    start = models.IntegerField(null=True, blank=True)
    end = models.IntegerField(null=True, blank=True)
    strand = models.IntegerField(default=0, choices=STRAND)
    length = models.IntegerField(null=True, blank=True)
    number_of_predicted_tmhs = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=200, null=True, blank=True)
    exp_number_of_aas_in_tmhs = models.FloatField(null=True, blank=True)
    exp_numberof_first_60_aas = models.FloatField(null=True, blank=True)
    total_prob_of_n_in = models.FloatField(null=True, blank=True)

class Helices(models.Model):
    tmh = models.ForeignKey(TransmembraneHelices, on_delete=models.CASCADE, related_name='helices')
    position = models.CharField(max_length=200, null=True, blank=True)
    self_start = models.IntegerField(null=True, blank=True)
    self_end = models.IntegerField(null=True, blank=True)

class VirulentFactor(models.Model):
    STRAND = (
        (0, '+'),
        (1, '-'),
    )
    plasmid = models.ForeignKey(Plasmid, on_delete=models.CASCADE, related_name="vfs")
    protein_id = models.CharField(max_length=200)
    orf_source = models.CharField(max_length=200, null=True, blank=True)
    start = models.IntegerField(null=True, blank=True)
    end = models.IntegerField(null=True, blank=True)
    strand = models.IntegerField(default=0, choices=STRAND)
    vf_seq_id = models.CharField(max_length=200, null=True, blank=True)
    identity = models.FloatField(null=True, blank=True)
    e_value = models.CharField(max_length=200, null=True, blank=True)
    gene_name = models.CharField(max_length=200, null=True, blank=True)
    product = models.CharField(max_length=200, null=True, blank=True)
    vf_id = models.CharField(max_length=200, null=True, blank=True)
    vf_name = models.CharField(max_length=200, null=True, blank=True)
    vf_fullname = models.TextField(blank=True, null=True)
    vf_cid = models.TextField(blank=True, null=True)
    vf_category = models.TextField(blank=True, null=True)
    characteristics = models.TextField(blank=True, null=True)
    structure = models.TextField(blank=True, null=True)
    function = models.TextField(blank=True, null=True)
    mechanism = models.TextField(blank=True, null=True)
    sequence = models.TextField(blank=True, null=True)

class Crispr(models.Model):
    plasmid = models.ForeignKey(Plasmid, on_delete=models.CASCADE, related_name="crisprs")
    cas_id = models.CharField(max_length=200)
    cas_start = models.IntegerField(null=True, blank=True)
    cas_end = models.IntegerField(null=True, blank=True)
    cas_subtype = models.CharField(max_length=200, null=True, blank=True)
    crispr_id = models.CharField(max_length=200)
    start = models.IntegerField(null=True, blank=True)
    end = models.IntegerField(null=True, blank=True)
    crispr_subtype = models.CharField(max_length=200, null=True, blank=True)
    cas_consenus_prediction = models.CharField(max_length=200, null=True, blank=True)
    consensus_repeat_sequence = models.TextField(blank=True, null=True)
    cas_genes = models.TextField(blank=True, null=True)

class Cluster(models.Model):
    cluster_id = models.CharField(max_length=200)
    avg_gc = models.FloatField(null=True, blank=True)
    avg_length = models.FloatField(null=True, blank=True)
    no_of_subclusters = models.IntegerField(max_length=200, null=True, blank=True)
    no_of_members = models.IntegerField(max_length=200, null=True, blank=True)

class Subcluster(models.Model):
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE, related_name="subclusters")
    subcluster_id = models.CharField(max_length=200)
    avg_gc = models.FloatField(null=True, blank=True)
    avg_length = models.FloatField(null=True, blank=True)
    no_of_members = models.IntegerField(max_length=200, null=True, blank=True)
    members = models.TextField(blank=True, null=True)