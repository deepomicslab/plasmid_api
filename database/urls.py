from database.views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.conf.urls import url

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
    url(r'^get_plasmid_fasta/(?P<plasmid_id>\d+)/$', get_plasmid_fasta, name='get_plasmid_fasta'),
    # url(r'^query_temp_data/(?P<device_id>[\w\-]+)/$', query_temp_data, name='query_temp_data'),
    url(r'^host_node/$', PlasmidHostNodeView.as_view()),
    url(r'^host_view/$', PlasmidHostView.as_view()),
    url(r'^get_plasmid_tmhs/$', get_plasmid_tmhs, name='get_plasmid_tmhs'),
    url(r'^get_cluster_plasmids/$', get_cluster_plasmids, name='get_cluster_plasmids'),
    url(r'^get_subcluster_plasmids/$', get_subcluster_plasmids, name='get_subcluster_plasmids'),
    url(r'^get_subcluster_plasmids/$', get_subcluster_plasmids, name='get_subcluster_plasmids'),
    url(r'^get_plasmid_crisprs/$', get_plasmid_crisprs, name='get_plasmid_crisprs'),

    # url(r'^get_plasmid_/$', get_plasmid_tmhs, name='get_plasmid_tmhs'),

]
