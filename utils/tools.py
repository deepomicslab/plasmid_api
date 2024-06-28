from Bio import SeqIO
from database.models import Plasmid
from database.serializers import PlasmidSerializer

def is_fasta(fatsapath):
    try:
        for record in SeqIO.parse(fatsapath, 'fasta'):
            pass
        return True
    except:
        return False

def is_multifasta(fatsapath):
    count = 0
    for record in SeqIO.parse(fatsapath, 'fasta'):
        count += 1
        if count > 2:
            return True
    return False



def uploadphagefastapreprocess(fatsapath):
    """preprocessed file to standard fasta format"""
    seq_dic = {}
    for seq_record in SeqIO.parse(fatsapath, "fasta"):
        seq_dic[seq_record.id] = str(seq_record.seq)

    f_out = open(fatsapath, "w")
    for seq_id in seq_dic:
        f_out.write(">" + seq_id + "\n")
        seq = seq_dic[seq_id]
        while len(seq) > 70:
            f_out.write(seq[:70] + "\n")
            seq = seq[70:]
        f_out.write(seq + "\n")
    f_out.close()


def fixIdLong(fatsapath):
    seq_dic = {}
    for seq_record in SeqIO.parse(fatsapath, "fasta"):
        seq_dic[seq_record.id] = str(seq_record.seq)
    f_out = open(fatsapath, "w")
    for seq_id in seq_dic:
        if len(seq_id) > 47:
            seqid = seq_id[-47:]
        else:
            seqid = seq_id
        f_out.write(">" + seqid + "\n")
        f_out.write(seq_dic[seq_id] + "\n")
    f_out.close()


def searchphagefasta(plasmidids, path):
    plasmids = Plasmid.objects.filter(plasmidid__in=plasmidids)
    plasmiddatas = PlasmidSerializer(plasmids, many=True).data
    with open(path, 'w') as f:
        for plasmiddata in plasmiddatas:
            with open(plasmiddata['fastapath'], 'r') as f1:
                f.write(f1.read()+'\n')