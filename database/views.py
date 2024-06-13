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
        queryset = Plasmid.objects.all()
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
            plasmid_id = int(self.request.GET['plasmid_id'])
            plasmid = Plasmid.objects.get(id=plasmid_id)
            q_expression |= Q(plasmid=plasmid)

        if 'protein_id' in self.request.GET:
            protein_id = self.request.GET['protein_id']
            q_expression &= Q(protein_id__icontains=protein_id)
        
        if 'search' in self.request.GET:
            searchstr = self.request.GET['search']
            q_expression |= Q(plasmid__plasmid_id__icontains=searchstr)
            q_expression |= Q(orf_source__icontains=searchstr)
            q_expression |= Q(product__icontains=searchstr)
            q_expression |= Q(function_source__icontains=searchstr)
            q_expression |= Q(cog_category__icontains=searchstr)

        if 'source' in self.request.GET:
            source = int(self.request.GET['source'])
            if source != -1:
                q_expression &= Q(plasmid__source=source)
        
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
            plasmid_id = int(self.request.GET['plasmid_id'])
            plasmid = Plasmid.objects.get(id=plasmid_id)
            q_expression &= Q(plasmid=plasmid)
        
        # if 'search' in self.request.GET:
        #     searchstr = self.request.GET['search']
        #     q_expression |= Q(plasmid__plasmid_id__icontains=searchstr)
        #     q_expression |= Q(protein_id__icontains=searchstr)
        #     q_expression |= Q(prediction__icontains=searchstr)
        
        # if 'source' in self.request.GET:
        #     source = int(self.request.GET['source'])
        #     if source != -1:
        #         print(source)
        #         q_expression &= Q(plasmid__source=source)
        
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
                    rank=rank, parent=node)
            else:
                queryset = HostNode.objects.filter(rank=rank)
            print(queryset)
            serializer = HostNodeSerializer(queryset, many=True)
            for i in serializer.data:
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
            plasmid_id = int(self.request.GET['plasmid_id'])
            plasmid = Plasmid.objects.get(id=plasmid_id)
            q_expression &= Q(plasmid=plasmid)
        
        if 'search' in self.request.GET:
            searchstr = self.request.GET['search']
            q_expression |= Q(plasmid__plasmid_id__icontains=searchstr)
            q_expression |= Q(protein_id__icontains=searchstr)
            q_expression |= Q(trna_type__icontains=searchstr)
        
        if 'source' in self.request.GET:
            source = int(self.request.GET['source'])
            if source != -1:
                print(source)
                q_expression &= Q(plasmid__source=source)
        
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
            plasmid_id = int(self.request.GET['plasmid_id'])
            plasmid = Plasmid.objects.get(id=plasmid_id)
            q_expression &= Q(plasmid=plasmid)
        
        if 'search' in self.request.GET:
            searchstr = self.request.GET['search']
            q_expression |= Q(plasmid__plasmid_id__icontains=searchstr)
            q_expression |= Q(protein_id__icontains=searchstr)
            q_expression |= Q(orf_source__icontains=searchstr)
            q_expression |= Q(product__icontains=searchstr)
        
        if 'source' in self.request.GET:
            source = int(self.request.GET['source'])
            if source != -1:
                print(source)
                q_expression &= Q(plasmid__source=source)
        
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
            plasmid_id = int(self.request.GET['plasmid_id'])
            plasmid = Plasmid.objects.get(id=plasmid_id)
            q_expression &= Q(plasmid=plasmid)
        
        if 'search' in self.request.GET:
            searchstr = self.request.GET['search']
            q_expression |= Q(plasmid__plasmid_id__icontains=searchstr)
            q_expression |= Q(region__icontains=searchstr)
            q_expression |= Q(most_similar_known_cluster__icontains=searchstr)
            q_expression |= Q(similarity__icontains=searchstr)
        
        if 'source' in self.request.GET:
            source = int(self.request.GET['source'])
            if source != -1:
                print(source)
                q_expression &= Q(plasmid__source=source)
        
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
            plasmid_id = int(self.request.GET['plasmid_id'])
            plasmid = Plasmid.objects.get(id=plasmid_id)
            q_expression &= Q(plasmid=plasmid)
        
        if 'search' in self.request.GET:
            searchstr = self.request.GET['search']
            q_expression |= Q(plasmid__plasmid_id__icontains=searchstr)
            q_expression |= Q(protein_id__icontains=searchstr)
            q_expression |= Q(prediction__icontains=searchstr)
        
        if 'source' in self.request.GET:
            source = int(self.request.GET['source'])
            if source != -1:
                print(source)
                q_expression &= Q(plasmid__source=source)
        
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
            plasmid_id = int(self.request.GET['plasmid_id'])
            plasmid = Plasmid.objects.get(id=plasmid_id)
            q_expression &= Q(plasmid=plasmid)
        
        if 'search' in self.request.GET:
            searchstr = self.request.GET['search']
            q_expression |= Q(plasmid__plasmid_id__icontains=searchstr)
            q_expression |= Q(protein_id__icontains=searchstr)
            q_expression |= Q(source__icontains=searchstr)
        
        if 'source' in self.request.GET:
            source = int(self.request.GET['source'])
            if source != -1:
                print(source)
                q_expression &= Q(plasmid__source=source)
        
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
            plasmid_id = int(self.request.GET['plasmid_id'])
            plasmid = Plasmid.objects.get(id=plasmid_id)
            q_expression &= Q(plasmid=plasmid)
        
        if 'search' in self.request.GET:
            searchstr = self.request.GET['search']
            q_expression |= Q(plasmid__plasmid_id__icontains=searchstr)
            q_expression |= Q(protein_id__icontains=searchstr)
            q_expression |= Q(orf_source__icontains=searchstr)
            q_expression |= Q(vf_category__icontains=searchstr)
        
        if 'source' in self.request.GET:
            source = int(self.request.GET['source'])
            if source != -1:
                print(source)
                q_expression &= Q(plasmid__source=source)
        
        queryset = queryset.filter(q_expression)
        return queryset

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_plasmid_tmhs(request):
    data = []
    plasmid_id = int(request.GET['plasmid_id'])
    plasmid = Plasmid.objects.get(id=plasmid_id)
    for tmh in plasmid.tmhs.all():
        print(tmh.helices.count())
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
                print(i)
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
                print(i)
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
    fasta = os.path.join(utils.root_path(), '../media/data/fasta/{0}.fasta'.format(plasmid.plasmid_id))
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
        print(sub.members)
        members = ast.literal_eval(sub.members)
        print(members)
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
    print(members)
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
    plasmid_id = int(request.GET['plasmid_id'])
    plasmid = Plasmid.objects.get(id=plasmid_id)
    cas_ids = []
    for crispr in plasmid.crisprs.all():
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
