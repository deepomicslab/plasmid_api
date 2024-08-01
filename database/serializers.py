from rest_framework import serializers
from plasmid_api import settings
from database.models import *
import os

class PlasmidSerializer(serializers.ModelSerializer):
    fastapath = serializers.SerializerMethodField()
    gbkpath = serializers.SerializerMethodField()
    gffpath = serializers.SerializerMethodField()
    sm = serializers.SerializerMethodField()
    class Meta:
        model = Plasmid
        fields = '__all__'

    def get_sm(self, obj):
        return SecondaryMetabolism.objects.filter(plasmid_id=obj.plasmid_id).count()

    def get_fastapath(self, obj):
        return os.path.join(settings.METADATA, '{0}/fasta/{1}.fasta'.format(obj.get_source_display(), obj.plasmid_id))

    def get_gbkpath(self, obj):
        return os.path.join(settings.METADATA, '{0}/gbk/{1}.gbk'.format(obj.get_source_display(), obj.plasmid_id))
    
    def get_gffpath(self, obj):
        return os.path.join(settings.METADATA, '{0}/gff/{1}.gff'.format(obj.get_source_display(), obj.plasmid_id))

class ProteinSerializer(serializers.ModelSerializer):
    # plasmid_id = serializers.CharField(source='plasmid.plasmid_id')
    plasmid = serializers.SerializerMethodField('get_plasmid_id')
    strand = serializers.CharField(
        source='get_strand_display'
    )

    def get_plasmid_id(self, protein):
        plasmid = Plasmid.objects.get(plasmid_id=protein.plasmid_id)
        return plasmid.id
    
    class Meta:
        model = Protein
        fields = '__all__'

class HostSerializer(serializers.ModelSerializer):
    # plasmid_id = serializers.CharField(source='plasmid.plasmid_id')
    # source = serializers.CharField(source='plasmid.source')
    plasmid = serializers.SerializerMethodField('get_plasmid_id')
    def get_plasmid_id(self, host):
        plasmid = Plasmid.objects.get(plasmid_id=host.plasmid_id)
        return plasmid.id
    class Meta:
        model = Host
        fields = '__all__'

class HostNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostNode
        fields = '__all__'

class tRNASerializer(serializers.ModelSerializer):
    # plasmid_id = serializers.CharField(source='plasmid.plasmid_id')
    # source = serializers.CharField(source='plasmid.source')
    plasmid = serializers.SerializerMethodField('get_plasmid_id')
    strand = serializers.CharField(
        source='get_strand_display'
    )
    def get_plasmid_id(self, protein):
        plasmid = Plasmid.objects.get(plasmid_id=protein.plasmid_id)
        return plasmid.id
    class Meta:
        model = tRNA
        fields = '__all__'

class AntimicrobialResistanceGeneSerializer(serializers.ModelSerializer):
    # plasmid_id = serializers.CharField(source='plasmid.plasmid_id')
    # source = serializers.CharField(source='plasmid.source')
    strand = serializers.CharField(
        source='get_strand_display'
    )
    plasmid = serializers.SerializerMethodField('get_plasmid_id')
    def get_plasmid_id(self, protein):
        plasmid = Plasmid.objects.get(plasmid_id=protein.plasmid_id)
        return plasmid.id
    class Meta:
        model = AntimicrobialResistanceGene
        fields = '__all__'

class SecondaryMetabolismSerializer(serializers.ModelSerializer):
    # plasmid_id = serializers.CharField(source='plasmid.plasmid_id')
    # source = serializers.CharField(source='plasmid.source')
    plasmid = serializers.SerializerMethodField('get_plasmid_id')
    def get_plasmid_id(self, protein):
        plasmid = Plasmid.objects.get(plasmid_id=protein.plasmid_id)
        return plasmid.id
    class Meta:
        model = SecondaryMetabolism
        fields = '__all__'
    

class SignalPeptidesSerializer(serializers.ModelSerializer):
    # plasmid_id = serializers.CharField(source='plasmid.plasmid_id')
    # source = serializers.CharField(source='plasmid.source')
    plasmid = serializers.SerializerMethodField('get_plasmid_id')
    strand = serializers.CharField(
        source='get_strand_display'
    )
    def get_plasmid_id(self, protein):
        plasmid = Plasmid.objects.get(plasmid_id=protein.plasmid_id)
        return plasmid.id
    class Meta:
        model = SignalPeptides
        fields = '__all__'

class HelicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Helices
        fields = '__all__'

class TransmembraneHelicesSerializer(serializers.ModelSerializer):
    # plasmid_id = serializers.CharField(source='plasmid.plasmid_id')
    # source = serializers.CharField(source='plasmid.source')
    plasmid = serializers.SerializerMethodField('get_plasmid_id')
    helices = HelicesSerializer(many=True, read_only=True)
    strand = serializers.CharField(
        source='get_strand_display'
    )
    def get_plasmid_id(self, protein):
        plasmid = Plasmid.objects.get(plasmid_id=protein.plasmid_id)
        return plasmid.id
    class Meta:
        model = TransmembraneHelices
        fields = '__all__'

class VirulentFactorSerializer(serializers.ModelSerializer):
    # plasmid_id = serializers.CharField(source='plasmid.plasmid_id')
    # source = serializers.CharField(source='plasmid.source')
    plasmid = serializers.SerializerMethodField('get_plasmid_id')
    strand = serializers.CharField(
        source='get_strand_display'
    )
    def get_plasmid_id(self, protein):
        plasmid = Plasmid.objects.get(plasmid_id=protein.plasmid_id)
        return plasmid.id
    class Meta:
        model = VirulentFactor
        fields = '__all__'
    
class CrisprSerializer(serializers.ModelSerializer):
    # plasmid_id = serializers.CharField(source='plasmid.plasmid_id')
    plasmid = serializers.SerializerMethodField('get_plasmid_id')
    def get_plasmid_id(self, protein):
        plasmid = Plasmid.objects.get(plasmid_id=protein.plasmid_id)
        return plasmid.id
    class Meta:
        model = Crispr
        fields = '__all__'

class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = '__all__'

class SubclusterSerializer(serializers.ModelSerializer):
    cluster_id = serializers.CharField(source='cluster.cluster_id')
    class Meta:
        model = Subcluster
        fields = '__all__'