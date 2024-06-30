from analysis.views import *
from rest_framework.routers import DefaultRouter
from django.urls import include, re_path, path

router = DefaultRouter()
# router.register(r'plasmid', PlasmidViewSet, basename='plasmid')


urlpatterns =  [
    path('', include(router.urls)),
    path('task_list/', task_list, name='task_list'),
    path('submit_task/', submit_task, name='submit_task'),
    path('submit_cluster_task/', submit_cluster_task, name='submit_cluster_task'),
    path('check_plasmid_ids/', check_plasmid_ids, name='check_plasmid_ids'),
    path('view_task_detail/', view_task_detail, name='view_task_detail'),
    path('view_task_log/', view_task_log, name='view_task_log'),
    path('view_task_result/', view_task_result, name='view_task_result'),
    path('view_task_result_modules/', view_task_result_modules, name='view_task_result_modules'),
    path('view_task_result_proteins/', view_task_result_proteins, name='view_task_result_proteins'),
    path('view_task_result_plasmid_detail/', view_task_result_plasmid_detail, name='view_task_result_plasmid_detail'),
    path('view_task_result_plasmid_fasta/', view_task_result_plasmid_fasta, name='view_task_result_plasmid_fasta'),
    path('view_task_result_tree/', view_task_result_tree, name='view_task_result_tree'),
    path('download_task_result_output_file/<path:path>/', download_task_result_output_file, name='download_task_result_output_file'),
    path('view_task_result_arvgs/', view_task_result_arvgs, name='view_task_result_arvgs'),
    path('view_task_result_transmembranes/', view_task_result_transmembranes, name='view_task_result_transmembranes'),
    path('view_task_trnas/', view_task_trnas, name='view_task_trnas'),

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
