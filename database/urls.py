from database.views import *
from rest_framework.routers import DefaultRouter
from django.urls import include, re_path, path

router = DefaultRouter()
router.register(r'plasmid', PlasmidViewSet, basename='plasmid')
router.register(r'protein', ProteinViewSet, basename='protein')
router.register(r'host', HostViewSet, basename='host')
router.register(r'trna', tRNAViewSet, basename='trna')
router.register(r'arg', AntimicrobialResistanceGeneViewSet, basename='arg')
router.register(r'sm', SecondaryMetabolismViewSet, basename='sm')
router.register(r'sp', SignalPeptidesViewSet, basename='sp')
router.register(r'tmh', TransmembraneHelicesViewSet, basename='tmh')
router.register(r'vf', VirulentFactorViewSet, basename='vf')
router.register(r'crispr', CrisprViewSet, basename='crispr')
router.register(r'cluster', ClusterViewSet, basename='cluster')
router.register(r'subcluster', SubclusterViewSet, basename='subcluster')

urlpatterns =  [
    path('', include(router.urls)),
    # url(r'^phone_login/$', phone_login, name='phone_login'),
    re_path(r'^get_plasmid_fasta/(?P<plasmid_id>\d+)/$', get_plasmid_fasta, name='get_plasmid_fasta'),
    # url(r'^query_temp_data/(?P<device_id>[\w\-]+)/$', query_temp_data, name='query_temp_data'),
    re_path(r'^host_node/$', PlasmidHostNodeView.as_view()),
    re_path(r'^host_view/$', PlasmidHostView.as_view()),
    re_path(r'^get_plasmid_tmhs/$', get_plasmid_tmhs, name='get_plasmid_tmhs'),
    re_path(r'^get_cluster_plasmids/$', get_cluster_plasmids, name='get_cluster_plasmids'),
    re_path(r'^get_subcluster_plasmids/$', get_subcluster_plasmids, name='get_subcluster_plasmids'),
    re_path(r'^get_subcluster_plasmids/$', get_subcluster_plasmids, name='get_subcluster_plasmids'),
    re_path(r'^get_plasmid_crisprs/$', get_plasmid_crisprs, name='get_plasmid_crisprs'),
    re_path(r'^get_database_overview/$', get_database_overview, name='get_database_overview'),
    re_path(r'^get_home_overview/$', get_home_overview, name='get_home_overview'),
    re_path(r'^plasmid_filter/$', plasmid_filter, name='plasmid_filter'),
    path('files/<path:path>/', downloadbypaath, name='downloadbypaath'),

    # url(r'^get_plasmid_/$', get_plasmid_tmhs, name='get_plasmid_tmhs'),
    re_path(r'^download_plasmid_fasta/$', download_plasmid_fasta, name='download_plasmid_fasta'),
    re_path(r'^download_plasmid_meta/$', download_plasmid_meta, name='download_plasmid_meta'),
    re_path(r'^download_plasmid_gbk/$', download_plasmid_gbk, name='download_plasmid_gbk'),
    re_path(r'^download_plasmid_gff/$', download_plasmid_gff, name='download_plasmid_gff'),
    re_path(r'^download_cluster_fasta/$', download_cluster_fasta, name='download_cluster_fasta'),

]
