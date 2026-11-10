from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

from django.db.models import Sum
from django.utils import timezone

import random


# Accounts models
from .models import (
    PGProfile,
    PasswordOTP
)


# Hostel models
from hostel.models import (
    Customer,
    Room,
    Rent,
    Payment,
    Expense
)

def register(request):

    if request.method == "POST":


        name = request.POST["name"]

        username = request.POST["username"]

        email = request.POST["email"]

        phone = request.POST["phone"]

        password = request.POST["password"]

        pg_name = request.POST["pg_name"]

        branch = request.POST["branch"]

        address = request.POST["address"]

        capacity = request.POST["capacity"]



        user = User.objects.create_user(

            username=username,

            email=email,

            password=password

        )


        user.first_name = name

        user.is_staff = True

        user.save()



        pg = PGProfile.objects.create(

            user=user,

            pg_name=pg_name,

            branch=branch,

            address=address,

            phone=phone,

            capacity=capacity

        )


        messages.success(

            request,

            f"Registration successful. Your PG ID is {pg.pg_id}"

        )


        return redirect("login")



    return render(

        request,

        "accounts/register.html"

    )



def login(request):

    if request.method == "POST":


        username = request.POST["username"]

        password = request.POST["password"]



        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:


            auth_login(
                request,
                user
            )


            # Check Owner

            if hasattr(user, "pgprofile"):

                return redirect(
                    "owner_dashboard"
                )



            # Check Customer

            elif hasattr(user, "customer"):

                return redirect(
                    "customer_dashboard"
                )


        else:

            messages.error(
                request,
                "Invalid username or password"
            )



    return render(
        request,
        "accounts/login.html"
    )


@login_required
def owner_dashboard(request):


    pg = request.user.pgprofile


    today = timezone.now()



    # Customer count

    customer_count = Customer.objects.filter(
        pg=pg
    ).count()



    # Room count

    room_count = Room.objects.count()



    # Pending rent count

    pending_rent = Rent.objects.filter(
        balance_amount__gt=0
    ).count()





    # Total monthly rent amount

    total_amount = Customer.objects.filter(
        pg=pg
    ).aggregate(
        total=Sum("rent_amount")
    )["total"] or 0





    # Received amount (current month)

    received_amount = Payment.objects.filter(

        customer__pg=pg,

        payment_date__month=today.month,

        payment_date__year=today.year

    ).aggregate(

        total=Sum("amount")

    )["total"] or 0





    # Balance amount

    balance_amount = (
        total_amount -
        received_amount
    )





    # Total expense current month

    total_expense = Expense.objects.filter(

        pg=pg,

        date__month=today.month,

        date__year=today.year

    ).aggregate(

        total=Sum("amount")

    )["total"] or 0





    # Profit

    profit = (
        received_amount -
        total_expense
    )





    return render(

        request,

        "accounts/owner_dashboard.html",

        {


        "customer_count":
        customer_count,


        "room_count":
        room_count,


        "pending_rent":
        pending_rent,


        "total_amount":
        total_amount,


        "received_amount":
        received_amount,


        "balance_amount":
        balance_amount,


        "total_expense":
        total_expense,


        "profit":
        profit

        }

    )
@login_required
def profile(request):

    pg = request.user.pgprofile

    return render(
        request,
        "accounts/profile.html",
        {
            "pg": pg
        }
    )
@login_required
def edit_profile(request):

    pg = request.user.pgprofile


    if request.method == "POST":


        request.user.first_name = request.POST["name"]

        request.user.email = request.POST["email"]

        request.user.save()



        pg.pg_name = request.POST["pg_name"]

        pg.branch = request.POST["branch"]

        pg.phone = request.POST["phone"]

        pg.address = request.POST["address"]

        pg.capacity = request.POST["capacity"]



        if request.FILES.get("profile_image"):

            pg.profile_image = request.FILES["profile_image"]



        pg.save()



        messages.success(
            request,
            "Profile updated successfully"
        )


        return redirect("profile")



    return render(
        request,
        "accounts/edit_profile.html",
        {
            "pg": pg
        }
    )
@login_required
def user_logout(request):
    
    logout(request)

    return redirect("login")
def forgot_password(request):
    
    if request.method == "POST":

        email = request.POST["email"]


        try:

            user = User.objects.get(
                email=email
            )


            otp = str(
                random.randint(100000, 999999)
            )


            PasswordOTP.objects.create(
                user=user,
                otp=otp
            )


            send_mail(
                "Password Reset OTP",
                f"Your OTP is {otp}",
                "yourgmail@gmail.com",
                [email],
                fail_silently=False
            )


            request.session["reset_email"] = email


            return redirect(
                "verify_otp"
            )


        except User.DoesNotExist:

            messages.error(
                request,
                "Email not registered"
            )


    return render(
        request,
        "accounts/forgot_password.html"
    )
def reset_password(request):
    
    email = request.session.get(
        "reset_email"
    )


    if request.method == "POST":

        password = request.POST["password"]

        confirm_password = request.POST["confirm_password"]


        if password == confirm_password:


            user = User.objects.get(
                email=email
            )


            user.set_password(
                password
            )

            user.save()


            messages.success(
                request,
                "Password reset successful. Login now."
            )


            return redirect(
                "login"
            )


        else:

            messages.error(
                request,
                "Passwords do not match"
            )


    return render(
        request,
        "accounts/reset_password.html"
    )
def verify_otp(request):
    
    email = request.session.get("reset_email")


    if not email:
        return redirect("forgot_password")


    if request.method == "POST":

        otp = request.POST["otp"]


        user = User.objects.get(
            email=email
        )


        otp_data = PasswordOTP.objects.filter(
            user=user,
            otp=otp
        ).last()



        if otp_data:

            return redirect(
                "reset_password"
            )


        else:

            messages.error(
                request,
                "Invalid OTP"
            )


    return render(
        request,
        "accounts/verify_otp.html"
    )