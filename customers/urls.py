from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name='create_customer'),
    path('update/<int:pk>', views.update, name='update_customer'),
    path('fetch/<int:pk>', views.fetch, name='fetch_customer'),

    path('create_analysis/<int:customer_id>', views.create_analysis),
    path('fetch_analysis/<int:customer_id>', views.fetch_analysis_by_id),
    path('update_analysis/<int:customer_id>', views.update_analysis),
    
    path('create_address/<int:customer_id>/', views.create_address),
    path('fetch_addresses_by_type/<int:customer_id>/<str:address_type>/', views.fetch_addresses_by_type),
    path('update_address_by_type/<int:customer_id>/<str:address_type>/', views.update_address_by_type),
    path('fetch_all_addresses/<int:customer_id>/', views.fetch_all_addresses_by_customer),
    
    path('create_kyc_details/<int:customer_id>/', views.create_kyc_details),
    path('fetch_kyc_details/<int:customer_id>/', views.fetch_kyc_details),
    path('update_kyc_details/<int:customer_id>/', views.update_kyc_details),
]