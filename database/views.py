from django.http import HttpResponse, StreamingHttpResponse, JsonResponse, FileResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from database.serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
from plasmid_api import settings
import os
from . import utils
from io import BytesIO
import ast
from django.db.models import Count
import json
from plasmid_api import settings
import pandas as pd
import random

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'pagesize'
    max_page_size = 10000

class PlasmidViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    # queryset = Plasmid.objects.all()
    serializer_class = PlasmidSerializer
    pagination_class = LargeResultsSetPagination
    
    def get_queryset(self):
        queryset = Plasmid.objects.all().order_by('unique_id')
        q_expression = Q()

        if 'search' in self.request.GET:
            searchstr = self.request.GET['search']
            q_expression |= Q(plasmid_id__icontains=searchstr)
            q_expression |= Q(topology__icontains=searchstr)
            q_expression |= Q(host__icontains=searchstr)
            q_expression |= Q(completeness__icontains=searchstr)
            q_expression |= Q(mob_type__icontains=searchstr)
            q_expression |= Q(mobility__icontains=searchstr)
            q_expression |= Q(cluster__icontains=searchstr)
            q_expression |= Q(subcluster__icontains=searchstr)

        if 'source' in self.request.GET:
            source = int(self.request.GET['source'])
            if source != -1:
                q_expression &= Q(source=source)
        queryset = queryset.filter(q_expression)
        if 'source' in self.request.GET:
            source = int(self.request.GET['source'])
            if source == -1:
                queryset = queryset.distinct('unique_id')
        return queryset

class ProteinViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    # queryset = Protein.objects.all()
    serializer_class = ProteinSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        queryset = Protein.objects.all()
        q_expression = Q()

        if 'plasmid_id' in self.request.GET:
            plasmid_id = self.request.GET['plasmid_id']
            plasmid = Plasmid.objects.get(id=plasmid_id)
            q_expression &= Q(plasmid_id=plasmid.plasmid_id)

        if 'protein_id' in self.request.GET:
            protein_id = self.request.GET['protein_id']
            q_expression &= Q(protein_id__icontains=protein_id)
        
        if 'search' in self.request.GET:
            searchstr = self.request.GET['search']
            q_expression |= Q(plasmid_id__icontains=searchstr)
            q_expression |= Q(orf_source__icontains=searchstr)
            q_expression |= Q(product__icontains=searchstr)
            q_expression |= Q(function_source__icontains=searchstr)
            q_expression |= Q(cog_category__icontains=searchstr)

        if 'source' in self.request.GET:
            source = int(self.request.GET['source'])
            if source != -1:
                q_expression &= Q(source=source)
        
        queryset = queryset.filter(q_expression)
        return queryset


class HostViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    queryset = Host.objects.all()
    serializer_class = HostSerializer
    pagination_class = LargeResultsSetPagination

class CrisprViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    # queryset = Crispr.objects.all()
    serializer_class = CrisprSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        queryset = Crispr.objects.all()
        q_expression = Q()

        if 'plasmid_id' in self.request.GET:
            plasmid_id = self.request.GET['plasmid_id']
            plasmid = Plasmid.objects.get(id=plasmid_id)
            q_expression &= Q(plasmid_id=plasmid.plasmid_id)
        
        if 'search' in self.request.GET:
            searchstr = self.request.GET['search']
            q_expression |= Q(plasmid_id__icontains=searchstr)
            # q_expression |= Q(trna_type__icontains=searchstr)
        
        if 'source' in self.request.GET:
            source = int(self.request.GET['source'])
            if source != -1:
                q_expression &= Q(source=source)
        
        queryset = queryset.filter(q_expression)
        return queryset

class ClusterViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer
    pagination_class = LargeResultsSetPagination

class SubclusterViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    # queryset = Subcluster.objects.all()
    serializer_class = SubclusterSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        queryset = Subcluster.objects.all()
        q_expression = Q()

        if 'cluster_id' in self.request.GET:
            cluster_id = int(self.request.GET['cluster_id'])
            cluster = Cluster.objects.get(id=cluster_id)
            q_expression &= Q(cluster=cluster)
        
        queryset = queryset.filter(q_expression)
        return queryset

class PlasmidHostNodeView(APIView):

    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()

        if querydict.get('rank') is not None:
            rank = querydict['rank']
            tree = []
            if querydict.get('node') is not None:
                node = querydict['node']
                queryset = HostNode.objects.filter(
                    rank=rank, parent=node).order_by('node')
            else:
                queryset = HostNode.objects.filter(rank=rank).order_by('node')
            serializer = HostNodeSerializer(queryset, many=True)
            for i in serializer.data:
                if i['node'] == '-':
                    continue
                treenode = {}
                # treenode['label'] = i['node']+'('+str(i['phagecount'])+')'
                treenode['label'] = i['node']
                treenode['count'] = i['plasmid_count']
                treenode['rank'] = i['rank']
                tree.append(treenode)
        return Response(tree)

class PlasmidHostView(APIView):
    def get(self, request, *args, **kwargs):
        hosts = request.query_params.dict()['host']
        if hosts == 'Others':
            excluded_values = ['Synergistota', 'Cyanobacteriota', 'Fusobacteriota','Verrucomicrobiota','Pseudomonadota','Bacillota','Campylobacterota']
            plasmids = Host.objects.exclude(phylum=excluded_values)
        else:
            rank = request.query_params.dict()['rank']
            if rank == 'Phylum':
                plasmids = Host.objects.filter(phylum=hosts)
            elif rank == 'Class':
                plasmids = Host.objects.filter(host_class=hosts)
            elif rank == 'Order':
                plasmids = Host.objects.filter(order=hosts)
            elif rank == 'Family':
                plasmids = Host.objects.filter(family=hosts)
            elif rank == 'Genus':
                plasmids = Host.objects.filter(genus=hosts)
            elif rank == 'Species':
                plasmids = Host.objects.filter(species=hosts)
            else:
                plasmids = Host.objects.filter(name=hosts)
        paginator = LargeResultsSetPagination()
        paginated_plasmids = paginator.paginate_queryset(
                plasmids, request, view=self)
        serializer = HostSerializer(paginated_plasmids, many=True)
        return paginator.get_paginated_response(serializer.data)

@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def host_filter(request):
    hostjson = json.loads(request.data['hosts'])
    total_qs = Host.objects.none()
    for checkednode in hostjson:
        hosts = checkednode['label']
        rank = checkednode['rank']
        if rank == 'Phylum':
            plasmids = Host.objects.filter(phylum=hosts)
        elif rank == 'Class':
            plasmids = Host.objects.filter(host_class=hosts)
        elif rank == 'Order':
            plasmids = Host.objects.filter(order=hosts)
        elif rank == 'Family':
            plasmids = Host.objects.filter(family=hosts)
        elif rank == 'Genus':
            plasmids = Host.objects.filter(genus=hosts)
        elif rank == 'Species':
            plasmids = Host.objects.filter(species=hosts)
        else:
            plasmids = Host.objects.filter(name=hosts)
        total_qs = plasmids | total_qs

    paginator = LargeResultsSetPagination()
    paginated_plasmids = paginator.paginate_queryset(
            total_qs, request)
    serializer = HostSerializer(paginated_plasmids, many=True)
    return paginator.get_paginated_response(serializer.data)

class tRNAViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    # queryset = tRNA.objects.all()
    serializer_class = tRNASerializer
    pagination_class = LargeResultsSetPagination
    
    def get_queryset(self):
        queryset = tRNA.objects.all()
        q_expression = Q()

        if 'plasmid_id' in self.request.GET:
            plasmid_id = self.request.GET['plasmid_id']
            plasmid = Plasmid.objects.get(id=plasmid_id)
            q_expression &= Q(plasmid_id=plasmid.plasmid_id)
        
        if 'search' in self.request.GET:
            searchstr = self.request.GET['search']
            q_expression |= Q(plasmid_id__icontains=searchstr)
            q_expression |= Q(trna_type__icontains=searchstr)
        
        if 'source' in self.request.GET:
            source = int(self.request.GET['source'])
            if source != -1:
                q_expression &= Q(source=source)
        
        queryset = queryset.filter(q_expression)
        return queryset

class AntimicrobialResistanceGeneViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    # queryset = AntimicrobialResistanceGene.objects.all()
    serializer_class = AntimicrobialResistanceGeneSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        queryset = AntimicrobialResistanceGene.objects.all()
        q_expression = Q()

        if 'plasmid_id' in self.request.GET:
            plasmid_id = self.request.GET['plasmid_id']
            plasmid = Plasmid.objects.get(id=plasmid_id)
            q_expression &= Q(plasmid_id=plasmid.plasmid_id)
        
        if 'search' in self.request.GET:
            searchstr = self.request.GET['search']
            q_expression |= Q(plasmid_id__icontains=searchstr)
            q_expression |= Q(protein_id__icontains=searchstr)
            q_expression |= Q(orf_source__icontains=searchstr)
            q_expression |= Q(product__icontains=searchstr)
        
        if 'source' in self.request.GET:
            source = int(self.request.GET['source'])
            if source != -1:
                q_expression &= Q(source=source)
        
        queryset = queryset.filter(q_expression)
        return queryset

class SecondaryMetabolismViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    # queryset = SecondaryMetabolism.objects.all()
    serializer_class = SecondaryMetabolismSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        queryset = SecondaryMetabolism.objects.all()
        q_expression = Q()

        if 'plasmid_id' in self.request.GET:
            plasmid_id = self.request.GET['plasmid_id']
            plasmid = Plasmid.objects.get(id=plasmid_id)
            q_expression &= Q(plasmid_id=plasmid.plasmid_id)
        
        if 'search' in self.request.GET:
            searchstr = self.request.GET['search']
            q_expression |= Q(plasmid_id__icontains=searchstr)
            q_expression |= Q(region__icontains=searchstr)
            q_expression |= Q(most_similar_known_cluster__icontains=searchstr)
            q_expression |= Q(similarity__icontains=searchstr)
        
        if 'source' in self.request.GET:
            source = int(self.request.GET['source'])
            if source != -1:
                q_expression &= Q(source=source)
        
        queryset = queryset.filter(q_expression)
        return queryset

class SignalPeptidesViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    # queryset = SignalPeptides.objects.all()
    serializer_class = SignalPeptidesSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        queryset = SignalPeptides.objects.all()
        q_expression = Q()

        if 'plasmid_id' in self.request.GET:
            plasmid_id = self.request.GET['plasmid_id']
            plasmid = Plasmid.objects.get(id=plasmid_id)
            q_expression &= Q(plasmid_id=plasmid.plasmid_id)
        
        if 'search' in self.request.GET:
            searchstr = self.request.GET['search']
            q_expression |= Q(plasmid_id__icontains=searchstr)
            q_expression |= Q(protein_id__icontains=searchstr)
            q_expression |= Q(prediction__icontains=searchstr)
        
        if 'source' in self.request.GET:
            source = int(self.request.GET['source'])
            if source != -1:
                q_expression &= Q(source=source)
        
        queryset = queryset.filter(q_expression)
        return queryset

class TransmembraneHelicesViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    # queryset = TransmembraneHelices.objects.all()
    serializer_class = TransmembraneHelicesSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        queryset = TransmembraneHelices.objects.all()
        q_expression = Q()

        if 'plasmid_id' in self.request.GET:
            plasmid_id = self.request.GET['plasmid_id']
            plasmid = Plasmid.objects.get(id=plasmid_id)
            q_expression &= Q(plasmid_id=plasmid.plasmid_id)
        
        if 'search' in self.request.GET:
            searchstr = self.request.GET['search']
            q_expression |= Q(plasmid_id__icontains=searchstr)
            q_expression |= Q(protein_id__icontains=searchstr)
            q_expression |= Q(source__icontains=searchstr)
        
        if 'source' in self.request.GET:
            source = int(self.request.GET['source'])
            if source != -1:
                q_expression &= Q(datasource=source)
        
        queryset = queryset.filter(q_expression)
        return queryset

class VirulentFactorViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    # queryset = VirulentFactor.objects.all()
    serializer_class = VirulentFactorSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        queryset = VirulentFactor.objects.all()
        q_expression = Q()

        if 'plasmid_id' in self.request.GET:
            plasmid_id = self.request.GET['plasmid_id']
            plasmid = Plasmid.objects.get(id=plasmid_id)
            q_expression &= Q(plasmid_id=plasmid.plasmid_id)
        
        if 'search' in self.request.GET:
            searchstr = self.request.GET['search']
            q_expression |= Q(plasmid_id__icontains=searchstr)
            q_expression |= Q(protein_id__icontains=searchstr)
            q_expression |= Q(orf_source__icontains=searchstr)
            q_expression |= Q(vf_category__icontains=searchstr)
        
        if 'source' in self.request.GET:
            source = int(self.request.GET['source'])
            if source != -1:
                q_expression &= Q(source=source)
        
        queryset = queryset.filter(q_expression)
        return queryset

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_plasmid_tmhs(request):
    data = []
    plasmid_id = request.GET['plasmid_id']
    plasmid = Plasmid.objects.get(id=plasmid_id)
    for tmh in TransmembraneHelices.objects.filter(plasmid_id=plasmid.plasmid_id).all():
        helices = tmh.helices.order_by('self_start')
        i = 0
        flag = False
        insidestart = ''
        insideend = ''
        TMhelixstart = ''
        TMhelixend = ''
        outsidestart = ''
        outsideend = ''
        for helice in helices:
            if helice.self_start == 1:
                if helice.position == 'inside':
                    insidestart = helice.self_start
                    insideend = helice.self_end
                if helice.position == 'TMhelix':
                    TMhelixstart = helice.self_start
                    TMhelixend = helice.self_end
                if helice.position == 'outside':
                    outsidestart = helice.self_start
                    outsideend = helice.self_end
                continue
            if i%2 == 0 and flag:
                data.append({
                    "id": tmh.id,
                    "protein_id": tmh.protein_id,
                    "plasmid_id": plasmid_id,
                    "length": tmh.length,
                    "insidestart": insidestart,
                    "insideend": insideend,
                    "TMhelixstart": TMhelixstart,
                    "TMhelixend": TMhelixend,
                    "outsidestart": outsidestart,
                    "outsideend": outsideend
                })
                insidestart = ''
                insideend = ''
                TMhelixstart = ''
                TMhelixend = ''
                outsidestart = ''
                outsideend = ''
                if helice.position == 'inside':
                    insidestart = helice.self_start
                    insideend = helice.self_end
                if helice.position == 'TMhelix':
                    TMhelixstart = helice.self_start
                    TMhelixend = helice.self_end
                if helice.position == 'outside':
                    outsidestart = helice.self_start
                    outsideend = helice.self_end
                i = i + 1
            else:
                if helice.position == 'inside':
                    insidestart = helice.self_start
                    insideend = helice.self_end
                if helice.position == 'TMhelix':
                    TMhelixstart = helice.self_start
                    TMhelixend = helice.self_end
                if helice.position == 'outside':
                    outsidestart = helice.self_start
                    outsideend = helice.self_end
                i = i + 1
                flag = True
            data.append({
                "id": tmh.id,
                "protein_id": tmh.protein_id,
                "plasmid_id": plasmid_id,
                "length": tmh.length,
                "insidestart": insidestart,
                "insideend": insideend,
                "TMhelixstart": TMhelixstart,
                "TMhelixend": TMhelixend,
                "outsidestart": outsidestart,
                "outsideend": outsideend
            })
    return Response(data)

@api_view(["GET"])
def get_plasmid_fasta(request, plasmid_id):
    plasmid = Plasmid.objects.get(id=plasmid_id)
    source = plasmid.get_source_display()
    fasta = os.path.join(utils.root_path(), '../media/data/{0}/fasta/{1}.fasta'.format(source, plasmid.plasmid_id))
    content = ''
    with open(fasta, 'r') as file:
        content = content+file.read()
    content_bytes = content.encode('utf-8')
    buffer = BytesIO(content_bytes)
    response = FileResponse(buffer)
    response['Content-Disposition'] = 'attachment; filename="plasmid.fasta"'
    response['Content-Type'] = 'text/plain'
    return response

@api_view(["GET"])
def get_cluster_plasmids(request):
    cluster_id = request.GET.get('cluster_id')
    cluster = Cluster.objects.get(id=cluster_id)
    data = []
    for sub in cluster.subclusters.all():
        members = ast.literal_eval(sub.members)
        for plasmid_id in members:
            try:
                plasmid = Plasmid.objects.get(plasmid_id=plasmid_id)
                data.append({
                    "id": plasmid.id,
                    "plasmid_id": plasmid.plasmid_id,
                    "source": plasmid.source,
                    "topology": plasmid.topology,
                    "length": plasmid.length,
                    "gc_content": plasmid.gc_content,
                    "host": plasmid.host,
                    "completeness": plasmid.completeness,
                    "mob_type": plasmid.mob_type,
                    "mobility": plasmid.mobility,
                    "cluster": plasmid.cluster,
                    "subcluster": plasmid.subcluster,
                },)
            except:
                pass
    return Response(data)

@api_view(["GET"])
def get_subcluster_plasmids(request):
    subcluster_id = request.GET.get('subcluster_id')
    subcluster = Subcluster.objects.get(id=subcluster_id)
    data = []
    
    members = ast.literal_eval(subcluster.members)
    for plasmid_id in members:
        try:
            plasmid = Plasmid.objects.get(plasmid_id=plasmid_id)
            data.append({
                "id": plasmid.id,
                "plasmid_id": plasmid.plasmid_id,
                "source": plasmid.source,
                "topology": plasmid.topology,
                "length": plasmid.length,
                "gc_content": plasmid.gc_content,
                "host": plasmid.host,
                "completeness": plasmid.completeness,
                "mob_type": plasmid.mob_type,
                "mobility": plasmid.mobility,
                "cluster": plasmid.cluster,
                "subcluster": plasmid.subcluster,
            },)
        except:
            pass
    return Response(data)

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_plasmid_crisprs(request):
    data = []
    plasmid_id = request.GET['plasmid_id']
    plasmid = Plasmid.objects.get(id=plasmid_id)
    cas_ids = []
    for crispr in Crispr.objects.filter(plasmid_id=plasmid.plasmid_id).all():
        if crispr.cas_id not in cas_ids:
            cas_ids.append(crispr.cas_id)
            data.append({
                "id": crispr.cas_id,
                "type": "Cas",
                "start":crispr.cas_start,
                "end": crispr.cas_end,
            })
        data.append({
            "id": crispr.crispr_id,
            "type": "CRISPR",
            "start":crispr.start,
            "end": crispr.end,
        })
    return Response(data)

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_database_overview(request):
    data = {
        "overview": {
            # "plasmid": Plasmid.objects.all().count(),
            # "host": HostNode.objects.all().count(),
            # "protein": Protein.objects.all().count(),
            # 'trna': tRNA.objects.all().count(),
            # 'arg': AntimicrobialResistanceGene.objects.all().count(),
            # 'sm': SecondaryMetabolism.objects.all().count(),
            # 'sp': SignalPeptides.objects.all().count(),
            # 'tmh': TransmembraneHelices.objects.all().count(),
            # 'vf': VirulentFactor.objects.all().count(),
            # 'crispr': Crispr.objects.all().count()
            "plasmid": 852600,
            "host": 9572,
            "protein": 25231059,
            "trna": 82718,
            "arg": 21090397,
            "sm": 40466,
            "sp": 2710395,
            "tmh": 5191488,
            "vf": 306218,
            "crispr": 4083
        },
        "hosts": [],
        "datasources": {
            "sources": [],
            "counts": [],
        },
        "datahosts": {
            "hosts": [],
            "counts": [],
        },
        "piedatasource": [],
        "piehosts": [],
        "treedata": []
    }
    for host in HostNode.objects.filter(rank='Phylum').order_by('-plasmid_count')[:11]:
        if host.node == '-':
            continue
        data['hosts'].append(host.node)
        data['datahosts']['hosts'].append(host.node)
        data['datahosts']['counts'].append(host.plasmid_count)
        data['piehosts'].append({
            "value": host.plasmid_count,
            "name": host.node
        })
        host_children = []
        for class_node in HostNode.objects.filter(rank='Class', parent=host.node):
            # if class_node.node == '-':
            #     continue
            class_children = []
            for order_node in HostNode.objects.filter(rank='Order', parent=class_node.node):
                # if order_node.node == '-':
                #     continue
                class_children.append({
                    'name': order_node.node, 
                    'value': order_node.plasmid_count, 
                    'children': [], 
                    'rank': 'Order'
                })
            host_children.append({
                'name': class_node.node, 
                'value': class_node.plasmid_count, 
                'children': class_children, 
                'rank': 'Class'
            })
        data['treedata'].append({
            'name': host.node, 
            'value': host.plasmid_count, 
            'children': host_children, 
            'rank': 'Phylum'
        })
    
    SOURCE_TYPE = (
        (1, 'IMG-PR'),
        (9, 'mMGEs'),
        (3, 'GenBank'),
        (4, 'RefSeq'),
        (0, 'PLSDB'),
        (2, 'COMPASS'),
        (5, 'EMBL'),
        (7, 'DDBJ'),
        (6, 'Kraken2'),
        (8, 'TPA'),
    )

    for source in SOURCE_TYPE:
        count = Plasmid.objects.filter(source=source[0]).count()
        data['datasources']['sources'].append(source[1])
        data['datasources']['counts'].append(count)
        data['piedatasource'].append({
            "value": count,
            "name": source[1]
        })

    # for host in HostNode.objects.filter(rank='Phylum').order_by('node'):
    #     if host.node == '-':
    #         continue
        
    data = {
        "overview": {
            "plasmid": 852600,
            "host": 9572,
            "protein": 25231059,
            "trna": 82718,
            "arg": 21090397,
            "sm": 40466,
            "sp": 2710395,
            "tmh": 5191488,
            "vf": 306218,
            "crispr": 4083
        },
        "hosts": [
            "Pseudomonadota",
            "Bacillota",
            "Bacteroidota",
            "Actinomycetota",
            "Spirochaetota",
            "Cyanobacteriota",
            "Campylobacterota",
            "Euryarchaeota",
            "Deinococcota",
            "Fusobacteriota"
        ],
        "datasources": {
            "sources": [
                "IMG-PR",
                "mMGE",
                "GenBank",
                "RefSeq",
                "PLSDB",
                "COMPASS",
                "ENA",
                "DDBJ",
                "Kraken2",
                "TPA"
            ],
            "counts": [
                699973,
                92492,
                91783,
                85995,
                50553,
                12084,
                6251,
                5320,
                898,
                7
            ]
        },
        "datahosts": {
            "hosts": [
                "Pseudomonadota",
                "Bacillota",
                "Bacteroidota",
                "Actinomycetota",
                "Spirochaetota",
                "Cyanobacteriota",
                "Campylobacterota",
                "Euryarchaeota",
                "Deinococcota",
                "Fusobacteriota"
            ],
            "counts": [
                286695,
                144001,
                43730,
                24815,
                14569,
                5158,
                3649,
                1995,
                1302,
                1261
            ]
        },
        "piedatasource": [
            {
                "value": 699973,
                "name": "IMG-PR"
            },
            {
                "value": 92492,
                "name": "mMGE"
            },
            {
                "value": 91783,
                "name": "GenBank"
            },
            {
                "value": 85995,
                "name": "RefSeq"
            },
            {
                "value": 50553,
                "name": "PLSDB"
            },
            {
                "value": 12084,
                "name": "COMPASS"
            },
            {
                "value": 6251,
                "name": "ENA"
            },
            {
                "value": 5320,
                "name": "DDBJ"
            },
            {
                "value": 898,
                "name": "Kraken2"
            },
            {
                "value": 7,
                "name": "TPA"
            }
        ],
        "piehosts": [
            {
                "value": 286695,
                "name": "Pseudomonadota"
            },
            {
                "value": 144001,
                "name": "Bacillota"
            },
            {
                "value": 43730,
                "name": "Bacteroidota"
            },
            {
                "value": 24815,
                "name": "Actinomycetota"
            },
            {
                "value": 14569,
                "name": "Spirochaetota"
            },
            {
                "value": 5158,
                "name": "Cyanobacteriota"
            },
            {
                "value": 3649,
                "name": "Campylobacterota"
            },
            {
                "value": 1995,
                "name": "Euryarchaeota"
            },
            {
                "value": 1302,
                "name": "Deinococcota"
            },
            {
                "value": 1261,
                "name": "Fusobacteriota"
            }
        ],
        "treedata": [
            {
                "name": "Pseudomonadota",
                "value": 286695,
                "children": [
                    {
                        "name": "Hydrogenophilia",
                        "value": 131,
                        "children": [
                            {
                                "name": "Hydrogenophilales",
                                "value": 131,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "-",
                        "value": 197,
                        "children": [
                            {
                                "name": "-",
                                "value": 12,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 3,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 2,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 5,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Mycoplasmoidales",
                                "value": 204,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 422457,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 39,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 6,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Peronosporales",
                                "value": 4,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 4,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 836,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Candidatus Absconditabacterales",
                                "value": 8,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Candidatus Fermentimicrarchaeales",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Candidatus Obscuribacterales",
                                "value": 63,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 3,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 5,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Caldicellulosiruptorales",
                                "value": 46,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 19,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 7,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 197,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Gammaproteobacteria",
                        "value": 226279,
                        "children": [
                            {
                                "name": "Lysobacterales",
                                "value": 5058,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Cardiobacteriales",
                                "value": 137,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Orbales",
                                "value": 53,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Acidiferrobacterales",
                                "value": 3,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Methylococcales",
                                "value": 276,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Pasteurellales",
                                "value": 2109,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Cellvibrionales",
                                "value": 75,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Thiotrichales",
                                "value": 1521,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Nevskiales",
                                "value": 7,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Moraxellales",
                                "value": 15067,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Oceanospirillales",
                                "value": 533,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Pseudomonadales",
                                "value": 9650,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Legionellales",
                                "value": 964,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Steroidobacterales",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Xanthomonadales",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Enterobacterales",
                                "value": 180987,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Aeromonadales",
                                "value": 2664,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Vibrionales",
                                "value": 4590,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1306,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Salinisphaerales",
                                "value": 7,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Chromatiales",
                                "value": 189,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Alteromonadales",
                                "value": 1081,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Alphaproteobacteria",
                        "value": 47160,
                        "children": [
                            {
                                "name": "Emcibacterales",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Rickettsiales",
                                "value": 430,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Hyphomonadales",
                                "value": 55,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Rhodobacterales",
                                "value": 10015,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Holosporales",
                                "value": 47,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Micropepsales",
                                "value": 3,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Candidatus Puniceispirillales",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Rhodothalassiales",
                                "value": 2,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Sphingomonadales",
                                "value": 5329,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Geminicoccales",
                                "value": 59,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Magnetococcales",
                                "value": 5,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Parvularculales",
                                "value": 4,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Hyphomicrobiales",
                                "value": 25625,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Rhodospirillales",
                                "value": 5300,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Maricaulales",
                                "value": 7,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Iodidimonadales",
                                "value": 2,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Kordiimonadales",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 40,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Caulobacterales",
                                "value": 232,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Candidatus Pelagibacterales",
                                "value": 2,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Betaproteobacteria",
                        "value": 12754,
                        "children": [
                            {
                                "name": "-",
                                "value": 24,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Burkholderiales",
                                "value": 10073,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Ferrovales",
                                "value": 4,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Neisseriales",
                                "value": 2112,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Nitrosomonadales",
                                "value": 270,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Rhodocyclales",
                                "value": 271,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Zetaproteobacteria",
                        "value": 5,
                        "children": [
                            {
                                "name": "Mariprofundales",
                                "value": 5,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Acidithiobacillia",
                        "value": 169,
                        "children": [
                            {
                                "name": "Acidithiobacillales",
                                "value": 169,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    }
                ],
                "rank": "Phylum"
            },
            {
                "name": "Bacillota",
                "value": 144001,
                "children": [
                    {
                        "name": "Bacilli",
                        "value": 82741,
                        "children": [
                            {
                                "name": "Lactobacillales",
                                "value": 37298,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Bacillales",
                                "value": 45016,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 427,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Tissierellia",
                        "value": 114,
                        "children": [
                            {
                                "name": "-",
                                "value": 4,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Tissierellales",
                                "value": 110,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Erysipelotrichia",
                        "value": 2172,
                        "children": [
                            {
                                "name": "Erysipelotrichales",
                                "value": 2172,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Negativicutes",
                        "value": 1311,
                        "children": [
                            {
                                "name": "-",
                                "value": 27,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Acidaminococcales",
                                "value": 179,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Selenomonadales",
                                "value": 590,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Veillonellales",
                                "value": 515,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Limnochordia",
                        "value": 1,
                        "children": [
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Clostridia",
                        "value": 57597,
                        "children": [
                            {
                                "name": "Halobacteroidales",
                                "value": 3,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Monoglobales",
                                "value": 22,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Eubacteriales",
                                "value": 23964,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Peptostreptococcales",
                                "value": 950,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Christensenellales",
                                "value": 291,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Lutisporales",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Natranaerobiales",
                                "value": 15,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Thermoanaerobacterales",
                                "value": 37,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 13118,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Acetivibrionales",
                                "value": 40,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Lachnospirales",
                                "value": 19151,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Saccharofermentanales",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Moorellales",
                                "value": 4,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "-",
                        "value": 65,
                        "children": [
                            {
                                "name": "-",
                                "value": 12,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 3,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 2,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 5,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Mycoplasmoidales",
                                "value": 204,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 422457,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 39,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 6,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Peronosporales",
                                "value": 4,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 4,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 836,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Candidatus Absconditabacterales",
                                "value": 8,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Candidatus Fermentimicrarchaeales",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Candidatus Obscuribacterales",
                                "value": 63,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 3,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 5,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Caldicellulosiruptorales",
                                "value": 46,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 19,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 7,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 197,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    }
                ],
                "rank": "Phylum"
            },
            {
                "name": "Bacteroidota",
                "value": 43730,
                "children": [
                    {
                        "name": "Saprospiria",
                        "value": 37,
                        "children": [
                            {
                                "name": "Saprospirales",
                                "value": 37,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Cytophagia",
                        "value": 939,
                        "children": [
                            {
                                "name": "Cytophagales",
                                "value": 939,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Bacteroidia",
                        "value": 41540,
                        "children": [
                            {
                                "name": "-",
                                "value": 11,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Bacteroidales",
                                "value": 41529,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Sphingobacteriia",
                        "value": 90,
                        "children": [
                            {
                                "name": "Sphingobacteriales",
                                "value": 90,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Chitinophagia",
                        "value": 19,
                        "children": [
                            {
                                "name": "Chitinophagales",
                                "value": 19,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "-",
                        "value": 7,
                        "children": [
                            {
                                "name": "-",
                                "value": 12,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 3,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 2,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 5,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Mycoplasmoidales",
                                "value": 204,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 422457,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 39,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 6,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Peronosporales",
                                "value": 4,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 4,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 836,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Candidatus Absconditabacterales",
                                "value": 8,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Candidatus Fermentimicrarchaeales",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Candidatus Obscuribacterales",
                                "value": 63,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 3,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 5,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Caldicellulosiruptorales",
                                "value": 46,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 19,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 7,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 197,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Flavobacteriia",
                        "value": 1098,
                        "children": [
                            {
                                "name": "Flavobacteriales",
                                "value": 1098,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    }
                ],
                "rank": "Phylum"
            },
            {
                "name": "Actinomycetota",
                "value": 24815,
                "children": [
                    {
                        "name": "Actinomycetes",
                        "value": 21835,
                        "children": [
                            {
                                "name": "-",
                                "value": 137,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Actinomycetales",
                                "value": 774,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Bifidobacteriales",
                                "value": 3417,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Candidatus Actinomarinales",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Candidatus Nanopelagicales",
                                "value": 2,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Cryptosporangiales",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Frankiales",
                                "value": 69,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Geodermatophilales",
                                "value": 28,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Glycomycetales",
                                "value": 8,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Jiangellales",
                                "value": 7,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Kineosporiales",
                                "value": 35,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Kitasatosporales",
                                "value": 5647,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Micrococcales",
                                "value": 3200,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Micromonosporales",
                                "value": 240,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Motilibacterales",
                                "value": 3,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Mycobacteriales",
                                "value": 6702,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Nakamurellales",
                                "value": 6,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Propionibacteriales",
                                "value": 793,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Pseudonocardiales",
                                "value": 417,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Streptosporangiales",
                                "value": 348,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Saccharomycetes",
                        "value": 5,
                        "children": [
                            {
                                "name": "Saccharomycetales",
                                "value": 5,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Saccharomycetales",
                                "value": 129,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Coriobacteriia",
                        "value": 2081,
                        "children": [
                            {
                                "name": "Coriobacteriales",
                                "value": 1986,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Eggerthellales",
                                "value": 95,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Acidimicrobiia",
                        "value": 19,
                        "children": [
                            {
                                "name": "Acidimicrobiales",
                                "value": 19,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Nitriliruptoria",
                        "value": 4,
                        "children": [
                            {
                                "name": "Euzebyales",
                                "value": 4,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "-",
                        "value": 836,
                        "children": [
                            {
                                "name": "-",
                                "value": 12,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 3,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 2,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 5,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Mycoplasmoidales",
                                "value": 204,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 422457,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 39,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 6,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Peronosporales",
                                "value": 4,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 4,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 836,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Candidatus Absconditabacterales",
                                "value": 8,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Candidatus Fermentimicrarchaeales",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Candidatus Obscuribacterales",
                                "value": 63,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 3,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 5,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Caldicellulosiruptorales",
                                "value": 46,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 19,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 7,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 197,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Rubrobacteria",
                        "value": 28,
                        "children": [
                            {
                                "name": "Rubrobacterales",
                                "value": 28,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Thermoleophilia",
                        "value": 7,
                        "children": [
                            {
                                "name": "Miltoncostaeales",
                                "value": 4,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Solirubrobacterales",
                                "value": 3,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    }
                ],
                "rank": "Phylum"
            },
            {
                "name": "Spirochaetota",
                "value": 14569,
                "children": [
                    {
                        "name": "Spirochaetia",
                        "value": 14569,
                        "children": [
                            {
                                "name": "Brachyspirales",
                                "value": 33,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Leptospirales",
                                "value": 756,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Spirochaetales",
                                "value": 13764,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Treponematales",
                                "value": 16,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    }
                ],
                "rank": "Phylum"
            },
            {
                "name": "Cyanobacteriota",
                "value": 5158,
                "children": [
                    {
                        "name": "Cyanophyceae",
                        "value": 5158,
                        "children": [
                            {
                                "name": "-",
                                "value": 11,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Acaryochloridales",
                                "value": 159,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Chroococcales",
                                "value": 1048,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Chroococcidiopsidales",
                                "value": 54,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Coleofasciculales",
                                "value": 49,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Cyanobacteriales",
                                "value": 12,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Desertifilales",
                                "value": 5,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Elainellales",
                                "value": 19,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Geitlerinematales",
                                "value": 2,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Gloeobacterales",
                                "value": 6,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Gomontiellales",
                                "value": 80,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Leptolyngbyales",
                                "value": 179,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Nodosilineales",
                                "value": 40,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Nostocales",
                                "value": 2816,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Oscillatoriales",
                                "value": 253,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Phormidesmiales",
                                "value": 5,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Pleurocapsales",
                                "value": 63,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Pseudanabaenales",
                                "value": 96,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Spirulinales",
                                "value": 3,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Synechococcales",
                                "value": 258,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    }
                ],
                "rank": "Phylum"
            },
            {
                "name": "Campylobacterota",
                "value": 3649,
                "children": [
                    {
                        "name": "Desulfurellia",
                        "value": 3,
                        "children": [
                            {
                                "name": "Desulfurellales",
                                "value": 3,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Epsilonproteobacteria",
                        "value": 3646,
                        "children": [
                            {
                                "name": "Campylobacterales",
                                "value": 3626,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Nautiliales",
                                "value": 20,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    }
                ],
                "rank": "Phylum"
            },
            {
                "name": "Euryarchaeota",
                "value": 1995,
                "children": [
                    {
                        "name": "Archaeoglobi",
                        "value": 4,
                        "children": [
                            {
                                "name": "Archaeoglobales",
                                "value": 4,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Halobacteria",
                        "value": 1838,
                        "children": [
                            {
                                "name": "Halobacteriales",
                                "value": 1838,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Methanobacteria",
                        "value": 25,
                        "children": [
                            {
                                "name": "Methanobacteriales",
                                "value": 25,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Methanococci",
                        "value": 24,
                        "children": [
                            {
                                "name": "Methanococcales",
                                "value": 24,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Methanomicrobia",
                        "value": 54,
                        "children": [
                            {
                                "name": "Methanosarcinales",
                                "value": 50,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Methanotrichales",
                                "value": 4,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Methanosarcinia",
                        "value": 6,
                        "children": [
                            {
                                "name": "Methanosarcinales",
                                "value": 4,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Methanotrichales",
                                "value": 2,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Stenosarchaea group",
                        "value": 3,
                        "children": [
                            {
                                "name": "Halobacteria",
                                "value": 3,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Thermococci",
                        "value": 41,
                        "children": [
                            {
                                "name": "Thermococcales",
                                "value": 41,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    }
                ],
                "rank": "Phylum"
            },
            {
                "name": "Deinococcota",
                "value": 1302,
                "children": [
                    {
                        "name": "Deinococci",
                        "value": 1302,
                        "children": [
                            {
                                "name": "Deinococcales",
                                "value": 548,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Thermales",
                                "value": 754,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    }
                ],
                "rank": "Phylum"
            },
            {
                "name": "Fusobacteriota",
                "value": 1261,
                "children": [
                    {
                        "name": "-",
                        "value": 6,
                        "children": [
                            {
                                "name": "-",
                                "value": 12,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 3,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 2,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 5,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Mycoplasmoidales",
                                "value": 204,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 422457,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 39,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 6,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Peronosporales",
                                "value": 4,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 4,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 836,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Candidatus Absconditabacterales",
                                "value": 8,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Candidatus Fermentimicrarchaeales",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 1,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Candidatus Obscuribacterales",
                                "value": 63,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 3,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 5,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "Caldicellulosiruptorales",
                                "value": 46,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 19,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 7,
                                "children": [],
                                "rank": "Order"
                            },
                            {
                                "name": "-",
                                "value": 197,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    },
                    {
                        "name": "Fusobacteriia",
                        "value": 1255,
                        "children": [
                            {
                                "name": "Fusobacteriales",
                                "value": 1255,
                                "children": [],
                                "rank": "Order"
                            }
                        ],
                        "rank": "Class"
                    }
                ],
                "rank": "Phylum"
            }
        ]
    }
    return Response(data)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_home_overview(request):
    # data = {
    #         "plasmid": Plasmid.objects.all().count(),
    #         "host": HostNode.objects.all().count(),
    #         "protein": Protein.objects.all().count(),
    #         'trna': tRNA.objects.all().count(),
    #         'arg': AntimicrobialResistanceGene.objects.all().count(),
    #         'sm': SecondaryMetabolism.objects.all().count(),
    #         'sp': SignalPeptides.objects.all().count(),
    #         'tmh': TransmembraneHelices.objects.all().count(),
    #         'vf': VirulentFactor.objects.all().count(),
    #         'crispr': Crispr.objects.all().count()
    #     }
    data = {
        "plasmid": 852600,
        "host": 9572,
        "protein": 25231059,
        "trna": 82718,
        "arg": 21090397,
        "sm": 40466,
        "sp": 2710395,
        "tmh": 5191488,
        "vf": 306218,
        "crispr": 4083
    }
    return Response(data)

@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def plasmid_filter(request):
    filterdatajson = json.loads(request.data['filterdata'])
    q_expression = Q()
    query = Plasmid.objects.filter(q_expression)
    if filterdatajson['HostType'] != '':
        host = filterdatajson['HostType']
        hosts = Host.objects.filter(phylum=host).values('plasmid_id')
        plasmid_ids = []
        for item in hosts:
            plasmid_ids.append(item['plasmid_id'])
        q_expression = Q(plasmid_id__in=plasmid_ids)
        query = query.filter(q_expression)
    if filterdatajson['cluster'] != '':
        cluster = filterdatajson['cluster']
        q_expression = Q(cluster=cluster)
        query = query.filter(q_expression)
    if filterdatajson['subcluster'] != '':
        subcluster = filterdatajson['subcluster']
        q_expression = Q(subcluster=subcluster)
        query = query.filter(q_expression)
    # if filterdatajson['quality'] != '':
    #     quality = filterdatajson['quality']
    #     q_expression &= Q(completeness__exact=quality)
    if filterdatajson['datasets'] != []:
        datasets = filterdatajson['datasets']
        q_expression = Q(source__in=datasets)
        query = query.filter(q_expression)
    # if filterdatajson['lifestyle'] != '' and filterdatajson['lifestyle'] != 'all':
    #     lifestyle = filterdatajson['lifestyle']
    #     qs = phage_lifestyle.objects.filter(lifestyle=lifestyle)
    #     q_expression &= Q(phage_lifestyle__in=qs)
    # if filterdatajson['Taxonomy'] != '':
    #     taxonomy = filterdatajson['Taxonomy']
    #     q_expression &= Q(taxonomy=taxonomy)
    length_s = filterdatajson['LengthS']*1000
    length_e = filterdatajson['LengthE']*1000
    q_expression = Q(length__gte=length_s, length__lte=length_e)
    query = query.filter(q_expression)
    gc_s = filterdatajson['gcContentS']/100
    gc_e = filterdatajson['gcContentE']/100
    q_expression = Q(gc_content__gte=gc_s, gc_content__lte=gc_e)
    query = query.filter(q_expression)
    # total_queryset = Plasmid.objects.filter(q_expression)
    paginator = LargeResultsSetPagination()
    paginated_plasmids = paginator.paginate_queryset(
        query, request)
    serializer = PlasmidSerializer(paginated_plasmids, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def downloadbypaath(request, path):

    file_path = settings.METADATA + path
    file = open(file_path, 'rb')
    response = FileResponse(file)
    filename = file.name.split('/')[-1]
    response['Content-Disposition'] = "attachment; filename="+filename
    if path.endswith('.gz'):
        response['Content-Type'] = 'application/x-gzip'
    else:   
        response['Content-Type'] = 'text/plain'
    return response

@api_view(["GET"])
def download_plasmid_fasta(request):
    querydict = request.query_params.dict()
    if 'plasmid_id' in querydict:
        plasmid_id = querydict['plasmid_id']
        plasmid = Plasmid.objects.get(id=plasmid_id)
        source = plasmid.get_source_display()
        fasta = os.path.join(utils.root_path(), '../media/data/{0}/fasta/{1}.fasta'.format(source, plasmid.plasmid_id))
        pathlist = [fasta]
    elif 'plasmid_ids' in querydict:
        plasmid_id = querydict['plasmid_ids']
        plasmid_ids = plasmid_id.split(',')
        plasmid_obj = Plasmid.objects.filter(id__in=plasmid_ids)
        pathlist = []
        for plasmid in plasmid_obj:
            source = plasmid.get_source_display()
            fasta = os.path.join(utils.root_path(), '../media/data/{0}/fasta/{1}.fasta'.format(source, plasmid.plasmid_id))
            pathlist.append(fasta)
    # else:
    #     file = open('/home/platform/phage_db/phage_data/data/phage_sequence/phage_fasta/All_fasta.tar.gz', 'rb')
    #     response = FileResponse(file)
    #     filename = file.name.split('/')[-1]
    #     response['Content-Disposition'] = "attachment; filename="+filename
    #     response['Content-Type'] = 'application/x-gzip'
    #     return response
        

    content = ''
    for path in pathlist:
        try:
            with open(path, 'r') as file:
                content = content+file.read()
        except:
            continue
    content_bytes = content.encode('utf-8')
    buffer = BytesIO(content_bytes)
    response = response = FileResponse(buffer)
    response['Content-Disposition'] = 'attachment; filename="sequence.fasta"'
    response['Content-Type'] = 'text/plain'

    return response

@api_view(["GET"])
def download_plasmid_gbk(request):
    querydict = request.query_params.dict()
    if 'plasmid_id' in querydict:
        plasmid_id = querydict['plasmid_id']
        plasmid = Plasmid.objects.get(id=plasmid_id)
        source = plasmid.get_source_display()
        gbk = os.path.join(utils.root_path(), '../media/data/{0}/gbk/{1}.gbk'.format(source, plasmid.plasmid_id))
        pathlist = [gbk]
    elif 'plasmid_ids' in querydict:
        plasmid_id = querydict['plasmid_ids']
        plasmid_ids = plasmid_id.split(',')
        plasmid_obj = Plasmid.objects.filter(id__in=plasmid_ids)
        pathlist = []
        for plasmid in plasmid_obj:
            source = plasmid.get_source_display()
            gbk = os.path.join(utils.root_path(), '../media/data/{0}/gbk/{1}.gbk'.format(source, plasmid.plasmid_id))
            pathlist.append(gbk)
    # else:
    #     file = open('/home/platform/phage_db/phage_data/data/phage_sequence/phage_fasta/All_fasta.tar.gz', 'rb')
    #     response = FileResponse(file)
    #     filename = file.name.split('/')[-1]
    #     response['Content-Disposition'] = "attachment; filename="+filename
    #     response['Content-Type'] = 'application/x-gzip'
    #     return response
        

    content = ''
    for path in pathlist:
        with open(path, 'r') as file:
            content = content+file.read()
    content_bytes = content.encode('utf-8')
    buffer = BytesIO(content_bytes)
    response = response = FileResponse(buffer)
    response['Content-Disposition'] = 'attachment; filename="sequence.gbk"'
    response['Content-Type'] = 'text/plain'

    return response

@api_view(["GET"])
def download_plasmid_gff(request):
    querydict = request.query_params.dict()
    if 'plasmid_id' in querydict:
        plasmid_id = querydict['plasmid_id']
        plasmid = Plasmid.objects.get(id=plasmid_id)
        source = plasmid.get_source_display()
        gff = os.path.join(utils.root_path(), '../media/data/{0}/gff/{1}.gff'.format(source, plasmid.plasmid_id))
        pathlist = [gff]
    elif 'plasmid_ids' in querydict:
        plasmid_id = querydict['plasmid_ids']
        plasmid_ids = plasmid_id.split(',')
        plasmid_obj = Plasmid.objects.filter(id__in=plasmid_ids)
        pathlist = []
        for plasmid in plasmid_obj:
            source = plasmid.get_source_display()
            gff = os.path.join(utils.root_path(), '../media/data/{0}/gff/{1}.gff'.format(source, plasmid.plasmid_id))
            pathlist.append(gff)
    # else:
    #     file = open('/home/platform/phage_db/phage_data/data/phage_sequence/phage_fasta/All_fasta.tar.gz', 'rb')
    #     response = FileResponse(file)
    #     filename = file.name.split('/')[-1]
    #     response['Content-Disposition'] = "attachment; filename="+filename
    #     response['Content-Type'] = 'application/x-gzip'
    #     return response
        

    content = ''
    for path in pathlist:
        try:
            with open(path, 'r') as file:
                content = content+file.read()
        except:
            continue
    content_bytes = content.encode('utf-8')
    buffer = BytesIO(content_bytes)
    response = response = FileResponse(buffer)
    response['Content-Disposition'] = 'attachment; filename="sequence.gff"'
    response['Content-Type'] = 'text/plain'

    return response

@api_view(["GET"])
def download_plasmid_meta(request):
    querydict = request.query_params.dict()
    if 'plasmid_id' in querydict:
        plasmid_id = querydict['plasmid_id']
        plasmid = Plasmid.objects.get(id=plasmid_id)
        plasmid_data = [PlasmidSerializer(plasmid).data]
    elif 'plasmid_ids' in querydict:
        plasmid_id = querydict['plasmid_ids']
        plasmid_ids = plasmid_id.split(',')
        plasmid_obj = Plasmid.objects.filter(id__in=plasmid_ids)
        plasmid_data = PlasmidSerializer(plasmid_obj, many=True).data
    #     file = open('/home/platform/phage_db/phage_data/data/phage_sequence/phage_fasta/All_fasta.tar.gz', 'rb')
    #     response = FileResponse(file)
    #     filename = file.name.split('/')[-1]
    #     response['Content-Disposition'] = "attachment; filename="+filename
    #     response['Content-Type'] = 'application/x-gzip'
    #     return response
    plasmidmetadata = pd.DataFrame(plasmid_data)
    tmppath = settings.TEMPPATH + \
        str(random.randint(1000, 9999))+"_phagemetadata.tsv"
    plasmidmetadata.to_csv(tmppath, sep="\t", index=False)
    file = open(tmppath, 'rb')
    response = FileResponse(file)
    response['Content-Disposition'] = 'attachment; filename="metadata.tsv"'
    response['Content-Type'] = 'text/plain'
    return response

@api_view(["GET"])
def download_cluster_fasta(request):
    querydict = request.query_params.dict()
    if 'clusterid' in querydict:
        pathlist = []
        clusterid = querydict['clusterid']
        cluster = Cluster.objects.get(id=clusterid)
        for subcluster in cluster.subclusters.all():
            members = ast.literal_eval(subcluster.members)
            for plasmid_id in members:
                try:
                    plasmid = Plasmid.objects.get(plasmid_id=plasmid_id)
                    source = plasmid.get_source_display()
                    fasta = os.path.join(utils.root_path(), '../media/data/{0}/fasta/{1}.fasta'.format(source, plasmid.plasmid_id))
                    pathlist.append(fasta)
                except:
                    pass
        filename=cluster.cluster_id+'.fasta'

    elif 'clusterids' in querydict:
        pathlist = []
        clusterids = querydict['clusterids']
        clusterids = clusterids.split(',')
        for cluster in Cluster.objects.filter(id__in=clusterids):
            for subcluster in cluster.subclusters.all():
                members = ast.literal_eval(subcluster.members)
                for plasmid_id in members:
                    try:
                        plasmid = Plasmid.objects.get(plasmid_id=plasmid_id)
                        source = plasmid.get_source_display()
                        fasta = os.path.join(utils.root_path(), '../media/data/{0}/fasta/{1}.fasta'.format(source, plasmid.plasmid_id))
                        pathlist.append(fasta)
                    except:
                        pass
        filename = 'cluster.fasta'
    # else:
    #     file = open('/home/platform/phage_db/phage_data/data/phage_sequence/phage_fasta/All_fasta.tar.gz', 'rb')
    #     response = FileResponse(file)
    #     filename = file.name.split('/')[-1]
    #     response['Content-Disposition'] = "attachment; filename="+filename
    #     response['Content-Type'] = 'application/x-gzip'
    #     return response
        

    content = ''
    for path in pathlist:
        try:
            with open(path, 'r') as file:
                content = content+file.read()
        except:
            continue
    content_bytes = content.encode('utf-8')
    buffer = BytesIO(content_bytes)
    response = response = FileResponse(buffer)
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)
    response['Content-Type'] = 'text/plain'

    return response

@api_view(["GET"])
def download_protein_pdb(request):
    querydict = request.query_params.dict()
    if 'protein_id' in querydict:
        protein_id = querydict['protein_id']
        if protein_id != 'undefined':
            protein = Protein.objects.get(id=protein_id)
            source = protein.get_source_display()
            pdb_folder = os.path.join(utils.root_path(), '../media/data/{0}/pdb'.format(source))
            pdb = os.path.join(utils.root_path(), '../media/data/{0}/pdb/{1}.pdb'.format(source, protein.protein_id))
            if not os.path.exists(pdb):
                if not os.path.exists(pdb_folder):
                    os.makedirs(pdb_folder)
                utils.esm_fold_pdb_api(protein.sequence, pdb)
            pathlist = [pdb]
            content = ''
            for path in pathlist:
                try:
                    with open(path, 'r') as file:
                        content = content+file.read()
                except:
                    continue
        else:
            sequence = querydict['sequence'][:-1]
            content = utils.esm_fold_pdb_api(sequence)
    
    content_bytes = content.encode('utf-8')
    buffer = BytesIO(content_bytes)
    response = response = FileResponse(buffer)
    response['Content-Disposition'] = 'attachment; filename="protein.pdb"'
    response['Content-Type'] = 'text/plain'

    return response

@api_view(["GET"])
def download_protein_cif(request):
    querydict = request.query_params.dict()
    if 'protein_id' in querydict:
        sequence = querydict['sequence'][:-1]
        content = utils.esm_fold_cif_api(sequence)
    
    content_bytes = content.encode('utf-8')
    buffer = BytesIO(content_bytes)
    response = response = FileResponse(buffer)
    response['Content-Disposition'] = 'attachment; filename="protein.cif"'
    response['Content-Type'] = 'text/plain'

    return response
