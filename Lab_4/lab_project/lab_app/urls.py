from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('clients/', views.clients, name='clients'),
    path('add_client/', views.add_client, name='add_client'),
    path('delete_client/<int:client_id>/', views.delete_client, name='delete_client'),
    path('client/edit/<int:client_id>/', views.edit_client, name='edit_client'),

    path('devices/', views.devices, name='devices'),
    path('add_device/', views.add_device, name='add_device'),
    path('device/edit/<str:serial_number>/', views.edit_device, name='edit_device'),
    path('delete_device/<str:serial_number>/', views.delete_device, name='delete_device'),

    path('workers/', views.workers, name='workers'),
    path('add_worker/', views.add_worker, name='add_worker'),
    path('delete_worker/<int:worker_id>/', views.delete_worker, name='delete_worker'),
    path('edit_worker/<int:worker_id>/', views.edit_worker, name='edit_worker'),

    path('repairs_count_by_client/', views.repairs_count_by_client_view, name='repairs_count_by_client'),
    path('in_progress_repair_applications/', views.in_progress_repair_applications_view, name='in_progress_repair_applications'),
    path('spare_parts_count/', views.spare_parts_count_view, name='spare_parts_count'),
    path('clients_with_multiple_repairs/', views.clients_with_multiple_repairs_view, name='clients_with_multiple_repairs'),
    path('spare_parts_sorted_by_price/', views.spare_parts_sorted_by_price_view, name='spare_parts_sorted_by_price'),
    path('devices_in_repair/', views.devices_in_repair_view, name='devices_in_repair'), 
    path('repair_application_statistics/', views.repair_application_statistics_pandas_view, name='repair_application_statistics'),
    path('plotly_dashboard/', views.plotly_dashboard, name='plotly_dashboard'),
    path('bokeh_dashboard/', views.bokeh_dashboard, name='bokeh_dashboard'),
    path('interactive_bokeh/', views.interactive_bokeh_plot, name='interactive_bokeh_plot'),
    path('update_plot/<int:slider_value>/', views.update_plot, name='update_plot'),

    path('api/repairs_count_by_client/', views.repairs_count_by_client, name='api_repairs_count_by_client'),
    path('api/in_progress_repairs/', views.in_progress_repair_applications, name='api_in_progress_repairs'),
    path('api/spare_parts_count/', views.spare_parts_count, name='api_spare_parts_count'),
    path('api/clients_with_multiple_repairs/', views.clients_with_multiple_repairs, name='api_clients_with_multiple_repairs'),
    path('api/spare_parts_sorted_by_price/', views.spare_parts_sorted_by_price, name='api_spare_parts_sorted_by_price'),
    path('api/devices_in_repair/', views.devices_in_repair, name='api_devices_in_repair'),
]
