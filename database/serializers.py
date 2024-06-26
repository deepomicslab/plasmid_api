from rest_framework import serializers
from database.models import *

class PlasmidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plasmid
        fields = '__all__'

class ProteinSerializer(serializers.ModelSerializer):
    # plasmid_id = serializers.CharField(source='plasmid.plasmid_id')
    strand = serializers.CharField(
        source='get_strand_display'
    )
    class Meta:
        model = Protein
        fields = '__all__'

class HostSerializer(serializers.ModelSerializer):
    # plasmid_id = serializers.CharField(source='plasmid.plasmid_id')
    source = serializers.CharField(source='plasmid.source')
    class Meta:
        model = Host
        fields = '__all__'

class HostNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostNode
        fields = '__all__'

class tRNASerializer(serializers.ModelSerializer):
    # plasmid_id = serializers.CharField(source='plasmid.plasmid_id')
    source = serializers.CharField(source='plasmid.source')
    strand = serializers.CharField(
        source='get_strand_display'
    )
    class Meta:
        model = tRNA
        fields = '__all__'

class AntimicrobialResistanceGeneSerializer(serializers.ModelSerializer):
    # plasmid_id = serializers.CharField(source='plasmid.plasmid_id')
    source = serializers.CharField(source='plasmid.source')
    strand = serializers.CharField(
        source='get_strand_display'
    )
    class Meta:
        model = AntimicrobialResistanceGene
        fields = '__all__'

class SecondaryMetabolismSerializer(serializers.ModelSerializer):
    # plasmid_id = serializers.CharField(source='plasmid.plasmid_id')
    source = serializers.CharField(source='plasmid.source')
    class Meta:
        model = SecondaryMetabolism
        fields = '__all__'
    

class SignalPeptidesSerializer(serializers.ModelSerializer):
    # plasmid_id = serializers.CharField(source='plasmid.plasmid_id')
    source = serializers.CharField(source='plasmid.source')
    strand = serializers.CharField(
        source='get_strand_display'
    )
    class Meta:
        model = SignalPeptides
        fields = '__all__'

class HelicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Helices
        fields = '__all__'

class TransmembraneHelicesSerializer(serializers.ModelSerializer):
    # plasmid_id = serializers.CharField(source='plasmid.plasmid_id')
    source = serializers.CharField(source='plasmid.source')
    helices = HelicesSerializer(many=True, read_only=True)
    strand = serializers.CharField(
        source='get_strand_display'
    )
    class Meta:
        model = TransmembraneHelices
        fields = '__all__'

class VirulentFactorSerializer(serializers.ModelSerializer):
    # plasmid_id = serializers.CharField(source='plasmid.plasmid_id')
    source = serializers.CharField(source='plasmid.source')
    strand = serializers.CharField(
        source='get_strand_display'
    )
    class Meta:
        model = VirulentFactor
        fields = '__all__'
    
class CrisprSerializer(serializers.ModelSerializer):
    # plasmid_id = serializers.CharField(source='plasmid.plasmid_id')
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