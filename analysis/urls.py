from analysis.views import *
from rest_framework.routers import DefaultRouter
from django.urls import include, re_path, path

router = DefaultRouter()
# router.register(r'plasmid', PlasmidViewSet, basename='plasmid')


urlpatterns =  [
    path('', include(router.urls)),
    path('tasks/list/', viewtask),
    # url(r'^phone_login/$', phone_login, name='phone_login'),
    # re_path(r'^get_plasmid_fasta/(?P<plasmid_id>\d+)/$', get_plasmid_fasta, name='get_plasmid_fasta'),
    # # url(r'^query_temp_data/(?P<device_id>[\w\-]+)/$', query_temp_data, name='query_temp_data'),
    # re_path(r'^host_node/$', PlasmidHostNodeView.as_view()),
    # re_path(r'^host_view/$', PlasmidHostView.as_view()),
    # re_path(r'^get_plasmid_tmhs/$', get_plasmid_tmhs, name='get_plasmid_tmhs'),
    # re_path(r'^get_cluster_plasmids/$', get_cluster_plasmids, name='get_cluster_plasmids'),
    # re_path(r'^get_subcluster_plasmids/$', get_subcluster_plasmids, name='get_subcluster_plasmids'),
    # re_path(r'^get_subcluster_plasmids/$', get_subcluster_plasmids, name='get_subcluster_plasmids'),
    # re_path(r'^get_plasmid_crisprs/$', get_plasmid_crisprs, name='get_plasmid_crisprs'),
    # re_path(r'^get_database_overview/$', get_database_overview, name='get_database_overview'),
    # re_path(r'^get_home_overview/$', get_home_overview, name='get_home_overview'),
    # re_path(r'^plasmid_filter/$', plasmid_filter, name='plasmid_filter'),

    # url(r'^get_plasmid_/$', get_plasmid_tmhs, name='get_plasmid_tmhs'),

]
