from django.urls import path
from . import views


urlpatterns = [

    path(
        "customers/",
        views.customer_list,
        name="customer_list"
    ),


    path(
        "customers/add/",
        views.add_customer,
        name="add_customer"
    ),


    path(
        "customers/edit/<int:id>/",
        views.edit_customer,
        name="edit_customer"
    ),


    path(
        "customers/delete/<int:id>/",
        views.delete_customer,
        name="delete_customer"
    ),
    path(
    "rooms/",
    views.rooms_list,
    name="room_list"
     ),


path(
    "rooms/add/",
    views.add_room,
    name="add_room"
),


path(
    "rooms/edit/<int:id>/",
    views.edit_room,
    name="edit_room"
),


path(
    "rooms/delete/<int:id>/",
    views.delete_room,
    name="delete_room"
),
path(
    "rent/",
    views.rent_list,
    name="rent_list"
),
path(
    "rent/customer/<int:id>/",
    views.customer_rent_details,
    name="customer_rent_details"
),
path(
    "rent/add/",
    views.add_rent,
    name="add_rent"
),
path(
    "rent/edit/<int:id>/",
    views.edit_rent,
    name="edit_rent"
),


path(
    "rent/delete/<int:id>/",
    views.delete_rent,
    name="delete_rent"
),
path(
    "electricity/",
    views.electricity_list,
    name="electricity_list"
),
path(
    "electricity/add/",
    views.add_electricity,
    name="add_electricity"
),
path(
    "electricity/details/<int:id>/",
    views.electricity_details,
    name="electricity_details"
),
path(
    "electricity/edit/<int:id>/",
    views.edit_electricity,
    name="edit_electricity"
),


path(
    "electricity/delete/<int:id>/",
    views.delete_electricity,
    name="delete_electricity"
),
path(
    "add-payment/",
    views.add_payment,
    name="add_payment"
),
path(
    "payments/",
    views.payment_list,
    name="payment_list"
),
path(
    "payment-details/<int:id>/",
    views.payment_details,
    name="payment_details"
),
path(
    "my-payments/",
    views.customer_payments,
    name="customer_payments"
),path(
    "get-customer-rents/",
    views.get_customer_rents,
    name="get_customer_rents"
),
path(
    "payment/delete/<int:id>/",
    views.delete_payment,
    name="delete_payment"
),
path(
    "payment/edit/<int:id>/",
    views.edit_payment,
    name="edit_payment"
),

    path(
        "notices/",
        views.notice_list,
        name="notice_list"
    ),


    path(
        "notice/add/",
        views.add_notice,
        name="add_notice"
    ),


    path(
        "notice/edit/<int:id>/",
        views.edit_notice,
        name="edit_notice"
    ),


    path(
        "notice/delete/<int:id>/",
        views.delete_notice,
        name="delete_notice"
    ),
path(
    "expenses/",
    views.expense_list,
    name="expense_list"
),


path(
    "expenses/edit/<int:id>/",
    views.edit_expense,
    name="edit_expense"
),


path(
    "expenses/delete/<int:id>/",
    views.delete_expense,
    name="delete_expense"
),
path(
    "expenses/add/",
    views.add_expense,
    name="add_expense"
),
path(
    "expense-report/",
    views.expense_report,
    name="expense_report"
),
path(
    "food-menu/",
    views.food_menu_list,
    name="food_menu_list"
),


path(
    "food-menu/add/",
    views.add_food_menu,
    name="add_food_menu"
),


path(
    "food-menu/edit/<int:id>/",
    views.edit_food_menu,
    name="edit_food_menu"
),
path(
    "food-menu/delete/<int:id>/",
    views.delete_food_menu,
    name="delete_food_menu"
),
path(
    "complaints/",
    views.complaint_list,
    name="complaint_list"
),


path(
    "complaints/solve/<int:id>/",
    views.solve_complaint,
    name="solve_complaint"
),
    path(
        "expense-report-pdf/",
        views.expense_report_pdf,
        name="expense_report_pdf"
    ),
    path(
    "expense-report-excel/",
    views.expense_report_excel,
    name="expense_report_excel"
),
]
