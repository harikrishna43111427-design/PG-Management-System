from django.urls import path
from . import views


urlpatterns = [


    path(
        "login/",
        views.customer_login,
        name="customer_login"
    ),


    path(
        "dashboard/",
        views.customer_dashboard,
        name="customer_dashboard"
    ),


    path(
        "profile/",
        views.customer_profile,
        name="customer_profile"
    ),


    path(
        "logout/",
        views.customer_logout,
        name="customer_logout"
    ),
    path(
    "room-details/",
    views.room_details,
    name="room_details"
),
    path(
    "electricity/",
    views.customer_electricity,
    name="customer_electricity"
),
    path(
    "rent/",
    views.customer_rent,
    name="customer_rent"
),
    path(
    "customer-payments/",
    views.customer_payments,
    name="customer_payments"
),
path(
    "notices/",
    views.customer_notices,
    name="customer_notices"
),
path(
    "today-menu/",
    views.today_food_menu,
    name="today_food_menu"
),

path(
    "complaints/",
    views.customer_complaints,
    name="customer_complaints"
),


path(
    "complaints/add/",
    views.add_complaint,
    name="add_complaint"
),


path(
    "complaints/edit/<int:id>/",
    views.edit_complaint,
    name="edit_complaint"
),
path(
    "complaints/delete/<int:id>/",
    views.delete_complaint,
    name="delete_complaint"
),

]