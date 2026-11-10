from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime
from hostel.models import (
    Complaint,
    Customer,
    Electricity,
    Notice,
    Payment,
    Rent,
    Room,
    FoodMenu,
)



def customer_login(request):

    if request.method == "POST":

        username = request.POST["username"]

        password = request.POST["password"]


        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:


            # Check customer account exists

            try:

                customer = Customer.objects.get(
                    user=user
                )


                login(
                    request,
                    user
                )


                return redirect(
                    "customer_dashboard"
                )


            except Customer.DoesNotExist:


                messages.error(
                    request,
                    "This is not a customer account"
                )


        else:

            messages.error(
                request,
                "Invalid username or password"
            )


    return render(
        request,
        "customers/login.html"
    )
from datetime import datetime


from datetime import datetime


@login_required
def customer_dashboard(request):

    customer = Customer.objects.get(
        user=request.user
    )


    payments = Payment.objects.filter(
        customer=customer
    )


    total_paid = payments.aggregate(
        total=Sum("amount")
    )["total"] or 0


    total_balance = payments.aggregate(
        total=Sum("balance_amount")
    )["total"] or 0



    # Food Menu

    today = datetime.today().strftime("%A")


    menu = FoodMenu.objects.filter(
        pg=customer.pg,
        day=today
    ).first()


    print("TODAY:", today)
    print("CUSTOMER PG:", customer.pg.id)
    print("MENU:", menu)



    return render(
        request,
        "customers/dashboard.html",
        {
            "customer": customer,
            "total_paid": total_paid,
            "total_balance": total_balance,
            "menu": menu
        }
    )
@login_required
def customer_profile(request):

    customer = Customer.objects.get(
        user=request.user
    )


    return render(
        request,
        "customers/profile.html",
        {
            "customer":customer
        }
    )
def customer_logout(request):
    
    logout(request)

    return redirect(
        "customer_login"
    )
@login_required
def room_details(request):

    customer = Customer.objects.get(
        user=request.user
    )

    return render(
        request,
        "customers/room_details.html",
        {
            "customer": customer
        }
    )
@login_required
def customer_electricity(request):

    customer = Customer.objects.get(
        user=request.user
    )


    electricity = Electricity.objects.filter(
        room=customer.room
    ).order_by(
        "-id"
    )


    total_electricity = 0


    for item in electricity:

        total_electricity += item.per_person_amount



    room = customer.room


    occupied_beds = 0


    if room:

        occupied_beds = Customer.objects.filter(
            room=room
        ).count()



    return render(
        request,
        "customers/electricity.html",
        {
            "customer": customer,

            "electricity": electricity,

            "room": room,

            "occupied_beds": occupied_beds,

            "total_electricity": total_electricity
        }
    )
def customer_rent(request):


    customer = Customer.objects.get(
        user=request.user
    )


    rents = Rent.objects.filter(
        customer=customer
    ).order_by(
        "-id"
    )


    return render(
        request,
        "customers/rent.html",
        {
            "customer": customer,
            "rents": rents
        }
    )
@login_required
def customer_payments(request):

    customer = get_object_or_404(
        Customer,
        user=request.user
    )


    payments = Payment.objects.filter(
        customer=customer
    ).order_by(
        "-id"
    )


    total_paid = payments.aggregate(
        total=Sum("amount")
    )["total"] or 0



    return render(
        request,
        "customers/payments.html",
        {
            "customer": customer,
            "payments": payments,
            "total_paid": total_paid
        }
    )
@login_required
def customer_notices(request):

    customer = Customer.objects.get(
        user=request.user
    )


    notices = Notice.objects.filter(
        pg=customer.pg
    ).order_by(
        "-id"
    )


    return render(
        request,
        "customers/notices.html",
        {
            "notices": notices
        }
    )
from datetime import datetime


@login_required
def today_food_menu(request):

    customer = request.user.customer

    pg = customer.pg


    today = datetime.today().strftime("%A")


    print("TODAY:", today)

    print("CUSTOMER PG:", pg)


    all_menu = FoodMenu.objects.filter(
        pg=pg
    )

    print("ALL MENU:", all_menu)


    menu = FoodMenu.objects.filter(
        pg=pg,
        day=today
    ).first()


    print("TODAY MENU:", menu)


    return render(
        request,
        "customers/today_menu.html",
        {
            "menu": menu
        }
    )
@login_required
def add_complaint(request):

    customer = Customer.objects.get(
        user=request.user
    )


    if request.method=="POST":

        Complaint.objects.create(

            pg=customer.pg,

            customer=customer,

            title=request.POST["title"],

            message=request.POST["message"]

        )


        messages.success(
            request,
            "Complaint submitted"
        )


        return redirect(
            "customer_complaints"
        )


    return render(
        request,
        "customers/add_complaint.html"
    )
@login_required
def customer_complaints(request):

    customer = Customer.objects.get(
        user=request.user
    )


    complaints = Complaint.objects.filter(
        customer=customer
    ).order_by("-id")


    return render(
        request,
        "customers/complaints.html",
        {
            "complaints":complaints
        }
    )
@login_required
def edit_complaint(request,id):

    complaint = get_object_or_404(
        Complaint,
        id=id,
        customer__user=request.user
    )


    if request.method=="POST":


        complaint.title=request.POST["title"]

        complaint.message=request.POST["message"]

        complaint.save()


        return redirect(
            "customer_complaints"
        )


    return render(
        request,
        "customers/edit_complaint.html",
        {
            "complaint":complaint
        }
    )
@login_required
def delete_complaint(request, id):

    complaint = get_object_or_404(
        Complaint,
        id=id,
        customer__user=request.user
    )

    complaint.delete()

    messages.success(
        request,
        "Complaint deleted successfully"
    )

    return redirect(
        "customer_complaints"
    )

