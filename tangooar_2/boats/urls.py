from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    
    # User
    path('users/create/', views.user_create_view, name='user_create'),
    path('users/update/<int:pk>/', views.user_update_view, name='user_update'),
    path('users/delete/<int:pk>/', views.user_delete_view, name='user_delete'),
    
    # Boat Owner Profile
    path('boat-owner-profiles/', views.boat_owner_profile_list_view, name='boat_owner_profiles'),
    path('boat-owner-profiles/create/', views.create_boat_owner_profile_view, name='create_boat_owner_profile'),
    path('boat-owner-profiles/update/<int:pk>/', views.update_boat_owner_profile_view, name='update_boat_owner_profile'),
    path('boat-owner-profiles/delete/<int:pk>/', views.delete_boat_owner_profile_view, name='delete_boat_owner_profile'),
    
    # Manager
    path('managers/', views.manager_list_view, name='manager_list'),
    path('managers/create/', views.create_manager_view, name='create_manager'),
    path('managers/update/<int:pk>/', views.update_manager_view, name='update_manager'),
    path('managers/delete/<int:pk>/', views.delete_manager_view, name='delete_manager'),
    
    # Customer
    path('customers/', views.customer_list_view, name='customer_list'),
    path('customers/create/', views.create_customer_view, name='create_customer'),
    path('customers/update/<int:pk>/', views.update_customer_view, name='update_customer'),
    path('customers/delete/<int:pk>/', views.delete_customer_view, name='delete_customer'),
    
    # Boats
    path('boats/', views.boat_list_view, name='boat_list'),
    path('boats/create/', views.create_boat_view, name='create_boat'),
    path('boats/update/<int:pk>/', views.update_boat_view, name='update_boat'),
    path('boats/delete/<int:pk>/', views.delete_boat_view, name='delete_boat'),
        
    path('cabins/', views.cabin_list_view, name='cabins'),
    path('schedule-calendars/', views.schedule_calendar_list_view, name='schedule_calendars'),
    path('customers/', views.customer_list_view, name='customers'),
    path('bookings/', views.booking_list_view, name='bookings'),
    path('tour-types/', views.tour_type_list_view, name='tour_types'),
    path('tour-packages/', views.tour_package_list_view, name='tour_packages'),
    path('tour-package-schedules/', views.tour_package_schedule_list_view, name='tour_package_schedules'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

