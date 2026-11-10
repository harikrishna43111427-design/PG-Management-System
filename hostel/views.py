from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.core.paginator import Paginator
from .models import FoodMenu

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.db.models import Sum

from django.contrib import messages

from django.http import JsonResponse


from .models import (
    Room,
    Customer,
    Rent,
    Electricity,
    Payment,
    Notice,
    Expense,
    FoodMenu,
    Complaint
)
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from django.http import HttpResponse


# Customer List

@login_required
def customer_list(request):

    pg = request.user.pgprofile


    customers = Customer.objects.filter(
        pg=pg
    )


    return render(
        request,
        "hostel/customers.html",
        {
            "customers": customers
        }
    )




# Add Customer

@login_required
def add_customer(request):

    pg = request.user.pgprofile

    rooms = Room.objects.all()

    if request.method == "POST":

        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]

        room_id = request.POST["room"]
        room = Room.objects.get(id=room_id)

        food = request.POST["food"]
        rent_amount = request.POST["rent_amount"]


        # Check username already exists
        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                "Username already exists. Please choose another username."
            )

            return redirect("add_customer")


        # Check email already exists
        if User.objects.filter(email=email).exists():

            messages.error(
                request,
                "Email already exists. Please use another email."
            )

            return redirect("add_customer")


        # Create login user
        user = User.objects.create_user(

            username=username,

            email=email,

            password=password,

            first_name=name

        )


        # Create customer profile
        Customer.objects.create(

            pg=pg,

            user=user,

            phone=phone,

            room=room,

            food=food,

            rent_amount=rent_amount

        )


        messages.success(
            request,
            "Customer added successfully"
        )

        return redirect("customer_list")


    return render(
        request,
        "hostel/add_customer.html",
        {
            "rooms": rooms
        }
    )
# Edit Customer
@login_required
def edit_customer(request, id):

    customer = Customer.objects.get(
        id=id
    )


    if request.method == "POST":

        customer.user.first_name = request.POST["name"]

        customer.phone = request.POST["phone"]

        customer.room_id = request.POST["room"]

        customer.room_type = request.POST["room_type"]

        customer.food = request.POST["food"]

        customer.rent_amount = request.POST["rent_amount"]


        customer.user.save()

        customer.save()


        messages.success(
            request,
            "Customer updated successfully"
        )


        return redirect(
            "customer_list"
        )


    return render(
        request,
        "hostel/edit_customer.html",
        {
            "customer": customer,
            "rooms": Room.objects.all()
        }
    )




# Delete Customer

@login_required
def delete_customer(request,id):

    customer = Customer.objects.get(
        id=id
    )

    customer.delete()


    messages.success(
        request,
        "Customer deleted"
    )


    return redirect(
        "customer_list"
    )
@login_required
def rooms_list(request):

    rooms = Room.objects.all()


    for room in rooms:

        room.occupied_count = Customer.objects.filter(
            room=room
        ).count()


    return render(
        request,
        "hostel/rooms.html",
        {
            "rooms": rooms
        }
    )
def add_room(request):

    if request.method == "POST":


        room_number = request.POST["room_number"]

        floor = request.POST["floor"]

        room_type = request.POST["room_type"]

        total_beds = request.POST["total_beds"]



        Room.objects.create(

            room_number=room_number,

            floor=floor,

            room_type=room_type,

            total_beds=total_beds

        )


        messages.success(
            request,
            "Room added successfully"
        )


        return redirect(
            "room_list"
        )



    return render(
        request,
        "hostel/add_room.html"
    )
@login_required
def edit_room(request, id):

    room = get_object_or_404(
        Room,
        id=id
    )


    if request.method == "POST":


        room.room_number = request.POST["room_number"]

        room.floor = request.POST["floor"]

        room.room_type = request.POST["room_type"]

        room.total_beds = request.POST["total_beds"]


        room.save()



        messages.success(
            request,
            "Room updated successfully"
        )


        return redirect(
            "room_list"
        )



    return render(
        request,
        "hostel/edit_room.html",
        {
            "room": room
        }
    )
@login_required
def delete_room(request, id):

    room = get_object_or_404(
        Room,
        id=id
    )


    room.delete()


    messages.success(
        request,
        "Room deleted successfully"
    )


    return redirect(
        "room_list"
    )
@login_required
def rent_list(request):
    
    customers = Customer.objects.all()


    customer_data = []


    for customer in customers:


        last_rent = Rent.objects.filter(
            customer=customer
        ).order_by(
            "-id"
        ).first()



        if last_rent:

            balance = last_rent.balance_amount

        else:

            balance = 0



        customer_data.append({

            "customer": customer,

            "balance": balance

        })



    return render(
        request,
        "hostel/rent_list.html",
        {
            "customer_data": customer_data
        }
    )
@login_required
def customer_rent_details(request, id):

    customer = get_object_or_404(
        Customer,
        id=id
    )


    rents = Rent.objects.filter(
        customer=customer
    ).order_by(
        "-id"
    )


    return render(
        request,
        "hostel/customer_rent_details.html",
        {
            "customer": customer,
            "rents": rents
        }
    )
@login_required
def add_rent(request):

    customers = Customer.objects.all()


    if request.method == "POST":


        customer_id = request.POST["customer"]


        customer = Customer.objects.get(
            id=customer_id
        )


        month = request.POST["month"]


        paid_amount = int(
            request.POST["paid_amount"]
        )


        due_date = request.POST["due_date"]



        # Get electricity amount automatically
        # Using customer room_number (your current model)

        electricity = Electricity.objects.filter(
        room=customer.room,
        month=month
         ).first()



        if electricity:

            electricity_amount = (
                electricity.per_person_amount
            )

        else:

            electricity_amount = 0




        # Get previous balance

        last_rent = Rent.objects.filter(
            customer=customer
        ).order_by(
            "-id"
        ).first()



        if last_rent:

            previous_balance = (
                last_rent.balance_amount
            )

        else:

            previous_balance = 0




        # Create Rent Record

        Rent.objects.create(

            customer=customer,

            month=month,

            room_rent=customer.rent_amount,

            electricity_amount=electricity_amount,

            previous_balance=previous_balance,

            paid_amount=paid_amount,

            due_date=due_date

        )



        messages.success(
            request,
            "Rent added successfully"
        )


        return redirect(
            "rent_list"
        )



    return render(
        request,
        "hostel/add_rent.html",
        {
            "customers": customers
        }
    )
@login_required
@login_required
def edit_rent(request, id):

    rent = get_object_or_404(
        Rent,
        id=id
    )


    if request.method == "POST":


        rent.electricity_amount = int(
            request.POST["electricity_amount"]
        )


        rent.paid_amount = int(
            request.POST["paid_amount"]
        )


        rent.due_date = request.POST["due_date"]


        rent.save()



        messages.success(
            request,
            "Rent updated successfully"
        )


        return redirect(
            "customer_rent_details",
            id=rent.customer.id
        )



    return render(
        request,
        "hostel/edit_rent.html",
        {
            "rent": rent
        }
    )
@login_required
def delete_rent(request, id):

    rent = get_object_or_404(
        Rent,
        id=id
    )


    customer_id = rent.customer.id


    rent.delete()


    messages.success(
        request,
        "Rent deleted successfully"
    )


    return redirect(
        "customer_rent_details",
        id=customer_id
    )
@login_required
def electricity_list(request):

    electricity = Electricity.objects.all().order_by("-id")


    for item in electricity:
        print(
            item.room.room_number,
            item.previous_units,
            item.current_units,
            item.units_used,
            item.total_amount
        )


    return render(
        request,
        "hostel/electricity_list.html",
        {
            "electricity": electricity
        }
    )
@login_required
def add_electricity(request):

    if request.method == "POST":

        room_id = request.POST["room"]

        month = request.POST["month"]


        previous_units = int(
            request.POST["previous_units"]
        )


        current_units = int(
            request.POST["current_units"]
        )


        room = get_object_or_404(
            Room,
            id=room_id
        )


        electricity = Electricity.objects.create(

            room=room,

            month=month,

            previous_units=previous_units,

            current_units=current_units

        )


        # Calculate units and amount immediately

        electricity.units_used = (
            current_units - previous_units
        )


        electricity.total_amount = (
            electricity.units_used *
            electricity.rate_per_unit
        )


        electricity.save()



        messages.success(
            request,
            "Electricity added successfully"
        )


        return redirect(
            "electricity_list"
        )



    return render(
        request,
        "hostel/add_electricity.html",
        {
            "rooms": Room.objects.all()
        }
    )


@login_required
def edit_electricity(request, id):

    electricity = get_object_or_404(
        Electricity,
        id=id
    )


    rooms = Room.objects.all()


    if request.method == "POST":

        electricity.room_id = request.POST["room"]

        electricity.month = request.POST["month"]


        electricity.current_units = int(
            request.POST["current_units"]
        )


        electricity.rate_per_unit = int(
            request.POST["rate_per_unit"]
        )


        electricity.save()


        messages.success(
            request,
            "Electricity updated successfully"
        )


        return redirect(
            "electricity_list"
        )


    return render(
        request,
        "hostel/edit_electricity.html",
        {
            "electricity": electricity,
            "rooms": rooms
        }
    )



@login_required
def delete_electricity(request, id):

    electricity = get_object_or_404(
        Electricity,
        id=id
    )


    electricity.delete()


    messages.success(
        request,
        "Electricity deleted successfully"
    )


    return redirect(
        "electricity_list"
    )
@login_required
def electricity_details(request, id):


    room = get_object_or_404(
        Room,
        id=id
    )


    electricity = Electricity.objects.filter(
        room=room
    ).order_by(
        "-id"
    )



    return render(
        request,
        "hostel/electricity_details.html",
        {
            "room": room,

            "electricity": electricity
        }
    )
@login_required
def add_payment(request):

    pg = request.user.pgprofile


    customers = Customer.objects.filter(
        pg=pg
    )


    if request.method == "POST":


        customer_id = request.POST["customer"]


        payment_type = request.POST["payment_type"]


        total_amount = int(
            request.POST["total_amount"]
        )


        amount = int(
            request.POST["amount"]
        )


        balance_amount = int(
            request.POST["balance_amount"]
        )


        payment_date = request.POST["payment_date"]


        payment_method = request.POST["payment_method"]


        transaction_id = request.POST.get(
            "transaction_id"
        )


        remarks = request.POST.get(
            "remarks"
        )



        customer = get_object_or_404(
            Customer,
            id=customer_id,
            pg=pg
        )



        Payment.objects.create(

            customer=customer,

            payment_type=payment_type,

            total_amount=total_amount,

            amount=amount,

            balance_amount=balance_amount,

            payment_date=payment_date,

            payment_method=payment_method,

            transaction_id=transaction_id,

            remarks=remarks

        )



        messages.success(
            request,
            "Payment added successfully"
        )


        return redirect(
            "payment_list"
        )



    return render(
        request,
        "hostel/add_payment.html",
        {
            "customers": customers
        }
    )
@login_required
def payment_list(request):

    pg = request.user.pgprofile


    payments = Payment.objects.filter(
        customer__pg=pg
    ).order_by(
        "-id"
    )


    return render(
        request,
        "hostel/payment_list.html",
        {
            "payments": payments
        }
    )
@login_required
def payment_details(request, id):

    pg = request.user.pgprofile


    payment = Payment.objects.get(
        id=id,
        customer__pg=pg
    )


    return render(
        request,
        "hostel/payment_details.html",
        {
            "payment": payment
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
def edit_payment(request, id):

    pg = request.user.pgprofile


    payment = get_object_or_404(
        Payment,
        id=id,
        customer__pg=pg
    )


    if request.method == "POST":


        payment.payment_type = request.POST["payment_type"]


        payment.amount = int(
            request.POST["amount"]
        )


        payment.payment_date = request.POST["payment_date"]


        payment.payment_method = request.POST["payment_method"]


        payment.transaction_id = request.POST.get(
            "transaction_id"
        )


        payment.remarks = request.POST.get(
            "remarks"
        )


        payment.save()



        messages.success(
            request,
            "Payment updated successfully"
        )


        return redirect(
            "payment_list"
        )



    return render(
        request,
        "hostel/edit_payment.html",
        {
            "payment": payment
        }
    )
@login_required
def delete_payment(request, id):

    pg = request.user.pgprofile


    payment = get_object_or_404(
        Payment,
        id=id,
        customer__pg=pg
    )


    payment.delete()


    messages.success(
        request,
        "Payment deleted successfully"
    )


    return redirect(
        "payment_list"
    )
@login_required
def get_customer_rents(request):

    customer_id = request.GET.get("customer_id")


    rents = Rent.objects.filter(
        customer_id=customer_id,
        balance_amount__gt=0
    )


    data = []


    for rent in rents:

        data.append({

            "id": rent.id,

            "month": rent.month,

            "total_amount": rent.total_amount,

            "balance_amount": rent.balance_amount

        })


    return JsonResponse(
        data,
        safe=False
    )
@login_required
def notice_list(request):

    pg = request.user.pgprofile


    notices = Notice.objects.filter(
        pg=pg
    ).order_by(
        "-id"
    )


    return render(
        request,
        "hostel/notice_list.html",
        {
            "notices": notices
        }
    )



@login_required
def add_notice(request):

    pg = request.user.pgprofile


    if request.method == "POST":

        title = request.POST["title"]

        message = request.POST["message"]

        is_important = (
            True
            if request.POST.get("is_important")
            else False
        )


        Notice.objects.create(

            pg=pg,

            title=title,

            message=message,

            is_important=is_important

        )


        messages.success(
            request,
            "Notice added successfully"
        )


        return redirect(
            "notice_list"
        )


    return render(
        request,
        "hostel/add_notice.html"
    )



@login_required
def edit_notice(request, id):

    notice = get_object_or_404(
        Notice,
        id=id
    )


    if request.method == "POST":

        notice.title = request.POST["title"]

        notice.message = request.POST["message"]

        notice.is_important = (
            True
            if request.POST.get("is_important")
            else False
        )


        notice.save()


        messages.success(
            request,
            "Notice updated successfully"
        )


        return redirect(
            "notice_list"
        )


    return render(
        request,
        "hostel/edit_notice.html",
        {
            "notice": notice
        }
    )



@login_required
def delete_notice(request, id):

    notice = get_object_or_404(
        Notice,
        id=id
    )


    notice.delete()


    messages.success(
        request,
        "Notice deleted successfully"
    )


    return redirect(
        "notice_list"
    )
@login_required
def add_expense(request):

    pg = request.user.pgprofile


    if request.method == "POST":


        category = request.POST.get(
            "category"
        )


        # FOOD
        if category == "FOOD":


            item_name = request.POST.get(
                "item_name"
            )


            if item_name == "ADD_NEW":


                item_name = request.POST.get(
                    "new_item"
                )



        # ELECTRICITY
        elif category == "ELECTRICITY":


            item_name = request.POST.get(
                "electricity_meter"
            )



        # WATER
        elif category == "WATER":


            item_name = request.POST.get(
                "water_item"
            )



        # MAINTENANCE / OTHER
        else:


            item_name = request.POST.get(
                "other_item"
            )



        quantity = request.POST.get(
            "quantity"
        )


        amount = int(
            request.POST.get("amount")
        )


        date = request.POST.get(
            "date"
        )


        remarks = request.POST.get(
            "remarks"
        )



        Expense.objects.create(

            pg=pg,

            category=category,

            item_name=item_name,

            quantity=quantity,

            amount=amount,

            date=date,

            remarks=remarks

        )



        messages.success(
            request,
            "Expense added successfully"
        )


        return redirect(
            "expense_list"
        )




    # Default food items

    default_items = [

        "Rice",
        "Dal",
        "Oil",
        "Sugar",
        "Salt",
        "Milk",
        "Curd",
        "Vegetables",
        "Fruits",
        "Eggs",
        "Gas Cylinder",

    ]



    # Previous saved items
    old_items = Expense.objects.filter(
    pg=pg,
    category="FOOD"
    ).values_list(
    "item_name",
    flat=True
    ).distinct()


    items = sorted(
        set(default_items) | set(old_items)
    )



    return render(
        request,
        "hostel/add_expense.html",
        {
            "items": items
        }
    )
@login_required
def expense_list(request):

    pg = request.user.pgprofile


    expenses = Expense.objects.filter(
        pg=pg
    ).order_by(
        "-date"
    )


    paginator = Paginator(
        expenses,
        10
    )   # 10 records per page


    page_number = request.GET.get(
        "page"
    )


    page_obj = paginator.get_page(
        page_number
    )


    return render(
        request,
        "hostel/expense_list.html",
        {
            "page_obj": page_obj
        }
    )



@login_required
def edit_expense(request,id):

    pg = request.user.pgprofile


    expense = get_object_or_404(
        Expense,
        id=id,
        pg=pg
    )


    if request.method=="POST":


        expense.category = request.POST["category"]

        expense.item_name = request.POST["item_name"]

        expense.quantity = request.POST.get(
            "quantity"
        )

        expense.amount = int(
            request.POST["amount"]
        )

        expense.date = request.POST["date"]

        expense.remarks = request.POST.get(
            "remarks"
        )


        expense.save()


        messages.success(
            request,
            "Expense updated successfully"
        )


        return redirect(
            "expense_list"
        )


    return render(
        request,
        "hostel/edit_expense.html",
        {
            "expense":expense
        }
    )




@login_required
def delete_expense(request,id):

    pg = request.user.pgprofile


    expense = get_object_or_404(
        Expense,
        id=id,
        pg=pg
    )


    expense.delete()


    messages.success(
        request,
        "Expense deleted successfully"
    )


    return redirect(
        "expense_list"
    )
@login_required
def expense_report(request):

    pg = request.user.pgprofile


    selected_month = request.GET.get(
        "month"
    )


    expenses = Expense.objects.filter(
        pg=pg
    )


    if selected_month:

        year, month = selected_month.split("-")


        expenses = expenses.filter(
            date__year=year,
            date__month=month
        )


    expenses = expenses.order_by(
        "-date"
    )


    total_expense = expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0



    return render(
        request,
        "hostel/expense_report.html",
        {
            "expenses": expenses,

            "total_expense": total_expense,

            "selected_month": selected_month
        }
    )
@login_required
def food_menu_list(request):

    pg = request.user.pgprofile


    menus = FoodMenu.objects.filter(
        pg=pg
    )


    return render(
        request,
        "hostel/food_menu_list.html",
        {
            "menus": menus
        }
    )
@login_required
def add_food_menu(request):

    pg = request.user.pgprofile


    if request.method == "POST":


        FoodMenu.objects.create(

            pg=pg,

            day=request.POST["day"],

            breakfast=request.POST["breakfast"],

            lunch=request.POST["lunch"],

            dinner=request.POST["dinner"]

        )


        messages.success(
            request,
            "Food menu added"
        )


        return redirect(
            "food_menu_list"
        )


    return render(
        request,
        "hostel/add_food_menu.html"
    )
@login_required
def edit_food_menu(request,id):

    menu = get_object_or_404(
        FoodMenu,
        id=id
    )


    if request.method=="POST":


        menu.day=request.POST["day"]

        menu.breakfast=request.POST["breakfast"]

        menu.lunch=request.POST["lunch"]

        menu.dinner=request.POST["dinner"]


        menu.save()


        return redirect(
            "food_menu_list"
        )


    return render(
        request,
        "hostel/edit_food_menu.html",
        {
            "menu":menu
        }
    )
@login_required
def delete_food_menu(request,id):

    menu=get_object_or_404(
        FoodMenu,
        id=id
    )


    menu.delete()


    return redirect(
        "food_menu_list"
    )
@login_required
def complaint_list(request):

    pg = request.user.pgprofile


    complaints = Complaint.objects.filter(
        pg=pg
    ).select_related(
        "customer",
        "customer__user",
        "customer__room"
    ).order_by(
        "-id"
    )


    return render(
        request,
        "hostel/complaint_list.html",
        {
            "complaints": complaints
        }
    )
@login_required
def solve_complaint(request,id):

    complaint=get_object_or_404(
        Complaint,
        id=id
    )


    complaint.status="SOLVED"

    complaint.save()


    return redirect(
        "complaint_list"
    )
@login_required
def expense_report_pdf(request):

    pg = request.user.pgprofile


    selected_month = request.GET.get(
        "month"
    )


    expenses = Expense.objects.filter(
        pg=pg
    )


    if selected_month:

        year, month = selected_month.split("-")

        expenses = expenses.filter(
            date__year=year,
            date__month=month
        )


    total_expense = expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0



    response = HttpResponse(
        content_type="application/pdf"
    )


    response["Content-Disposition"] = (
        'attachment; filename="expense_report.pdf"'
    )



    pdf = canvas.Canvas(response)



    pdf.setFont(
        "Helvetica-Bold",
        16
    )


    pdf.drawString(
        50,
        800,
        "PG Expense Report"
    )



    pdf.setFont(
        "Helvetica",
        12
    )


    y = 760


    for expense in expenses:


        text = (
            f"{expense.date} | "
            f"{expense.item_name} | "
            f"{expense.category} | "
            f"Rs.{expense.amount}"
        )


        pdf.drawString(
            50,
            y,
            text
        )


        y -= 25



    pdf.drawString(
        50,
        y-20,
        f"Total Expense: Rs.{total_expense}"
    )



    pdf.save()


    return response
@login_required
def expense_report_excel(request):

    pg = request.user.pgprofile


    selected_month = request.GET.get(
        "month"
    )


    expenses = Expense.objects.filter(
        pg=pg
    )


    if selected_month:

        year, month = selected_month.split("-")


        expenses = expenses.filter(
            date__year=year,
            date__month=month
        )



    workbook = Workbook()


    sheet = workbook.active


    sheet.title = "Expense Report"



    sheet.append(
        [
            "Date",
            "Item",
            "Category",
            "Amount"
        ]
    )



    total = 0



    for expense in expenses:


        sheet.append(
            [
                str(expense.date),
                expense.item_name,
                expense.category,
                expense.amount
            ]
        )


        total += expense.amount



    sheet.append([])


    sheet.append(
        [
            "",
            "",
            "Total Expense",
            total
        ]
    )



    response = HttpResponse(
        content_type=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


    response["Content-Disposition"] = (
        'attachment; filename="expense_report.xlsx"'
    )


    workbook.save(response)


    return response