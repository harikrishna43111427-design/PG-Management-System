from django.db import models
from django.contrib.auth.models import User
from accounts.models import PGProfile



# ROOM MODEL
class Room(models.Model):

    ROOM_TYPE = [
        ("AC", "AC"),
        ("NON AC", "Non AC"),
    ]


    room_number = models.CharField(
        max_length=20,
        unique=True
    )


    floor = models.CharField(
        max_length=20
    )


    room_type = models.CharField(
        max_length=10,
        choices=ROOM_TYPE,
        default="NON AC"
    )


    total_beds = models.IntegerField(
        default=0
    )


    def occupied_beds(self):

        return Customer.objects.filter(
            room=self
        ).count()



    def available_beds(self):

        return (
            self.total_beds -
            self.occupied_beds()
        )



    def __str__(self):

        return self.room_number





# CUSTOMER MODEL
class Customer(models.Model):

    pg = models.ForeignKey(
        PGProfile,
        on_delete=models.CASCADE
    )


    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )


    phone = models.CharField(
        max_length=10
    )


    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


    room_type = models.CharField(
        max_length=10,
        choices=[
            ("AC", "AC"),
            ("NON AC", "Non AC"),
        ],
        default="NON AC"
    )


    food = models.CharField(
        max_length=20,
        choices=[
            ("WITH FOOD", "With Food"),
            ("WITHOUT FOOD", "Without Food"),
        ],
        default="WITH FOOD"
    )


    rent_amount = models.IntegerField(
        default=0
    )


    joining_date = models.DateField(
        auto_now_add=True
    )



    def __str__(self):

        return self.user.first_name





# RENT MODEL
class Rent(models.Model):

    STATUS_CHOICES = [

        ("PAID", "Paid"),
        ("PARTIAL", "Partial"),
        ("PENDING", "Pending"),

    ]


    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )


    month = models.CharField(
        max_length=20
    )


    room_rent = models.IntegerField(
        default=0
    )


    electricity_amount = models.IntegerField(
        default=0
    )


    previous_balance = models.IntegerField(
        default=0
    )


    total_amount = models.IntegerField(
        default=0
    )


    paid_amount = models.IntegerField(
        default=0
    )


    balance_amount = models.IntegerField(
        default=0
    )


    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING"
    )


    due_date = models.DateField(
        null=True,
        blank=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )



    def save(self,*args,**kwargs):

        self.total_amount = (
            self.room_rent +
            self.electricity_amount +
            self.previous_balance
        )


        self.balance_amount = (
            self.total_amount -
            self.paid_amount
        )


        if self.balance_amount == 0:
            self.status = "PAID"

        elif self.paid_amount > 0:
            self.status = "PARTIAL"

        else:
            self.status = "PENDING"


        super().save(*args,**kwargs)
class Payment(models.Model):
    
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )


    payment_type = models.CharField(
        max_length=20,
        choices=[
            ("RENT","Rent"),
            ("BALANCE","Balance"),
        ]
    )


    total_amount = models.IntegerField(
        default=0
    )


    amount = models.IntegerField(
        default=0
    )


    balance_amount = models.IntegerField(
        default=0
    )


    payment_date = models.DateField()


    payment_method = models.CharField(
        max_length=20,
        choices=[
            ("CASH","Cash"),
            ("UPI","UPI"),
            ("BANK","Bank Transfer"),
        ],
        default="UPI"
    )


    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )


    remarks = models.TextField(
        blank=True,
        null=True
    )


    def save(self,*args,**kwargs):

        self.balance_amount = (
            self.total_amount - self.amount
        )

        super().save(*args,**kwargs)


    def __str__(self):

        return (
            self.customer.user.first_name
            +
            " - ₹"
            +
            str(self.amount)
        )


class Electricity(models.Model):
    
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE
    )


    month = models.CharField(
        max_length=20
    )


    previous_units = models.IntegerField(
        default=0
    )


    current_units = models.IntegerField(
        default=0
    )


    units_used = models.IntegerField(
        default=0
    )


    rate_per_unit = models.IntegerField(
        default=12
    )


    total_amount = models.IntegerField(
        default=0
    )


    per_person_amount = models.IntegerField(
        default=0
    )


    created_date = models.DateField(
        auto_now_add=True
    )


    def save(self, *args, **kwargs):

        self.previous_units = int(
            self.previous_units
        )

        self.current_units = int(
            self.current_units
        )


        self.units_used = (
            self.current_units -
            self.previous_units
        )


        self.total_amount = (
            self.units_used *
            self.rate_per_unit
        )


        occupied_beds = Customer.objects.filter(
            room=self.room
        ).count()


        if occupied_beds > 0:

            self.per_person_amount = (
                self.total_amount //
                occupied_beds
            )

        else:

            self.per_person_amount = 0


        super().save(*args, **kwargs)



    def __str__(self):

        return (
            self.room.room_number
            +
            " - "
            +
            self.month
        )
class Notice(models.Model):
    
    pg = models.ForeignKey(
        PGProfile,
        on_delete=models.CASCADE
    )


    title = models.CharField(
        max_length=200
    )


    message = models.TextField()


    date = models.DateField(
        auto_now_add=True
    )


    is_important = models.BooleanField(
        default=False
    )


    def __str__(self):

        return self.title
class Expense(models.Model):
    
    CATEGORY_CHOICES = [

        ("FOOD", "Food"),

        ("ELECTRICITY", "Electricity"),

        ("WATER", "Water"),

        ("MAINTENANCE", "Maintenance"),

        ("OTHER", "Other"),

    ]


    FOOD_ITEMS = [

        ("Rice", "Rice"),

        ("Dal", "Dal"),

        ("Oil", "Oil"),

        ("Sugar", "Sugar"),

        ("Salt", "Salt"),

        ("Milk", "Milk"),

        ("Curd", "Curd"),

        ("Vegetables", "Vegetables"),

        ("Fruits", "Fruits"),

        ("Eggs", "Eggs"),

        ("Gas Cylinder", "Gas Cylinder"),

        ("Other", "Other"),

    ]


    pg = models.ForeignKey(

        PGProfile,

        on_delete=models.CASCADE

    )


    category = models.CharField(

        max_length=20,

        choices=CATEGORY_CHOICES

    )


    item_name = models.CharField(

        max_length=100

    )


    quantity = models.CharField(

        max_length=50,

        blank=True,

        null=True

    )


    amount = models.IntegerField(

        default=0

    )


    date = models.DateField()


    remarks = models.TextField(

        blank=True,

        null=True

    )


    def __str__(self):

        return self.item_name
class FoodMenu(models.Model):
    
    DAYS = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    ]


    pg = models.ForeignKey(
        PGProfile,
        on_delete=models.CASCADE
    )


    day = models.CharField(
        max_length=20,
        choices=DAYS
    )


    breakfast = models.CharField(
        max_length=200
    )


    lunch = models.CharField(
        max_length=200
    )


    dinner = models.CharField(
        max_length=200
    )


    def __str__(self):

        return self.day
class Complaint(models.Model):
    
    STATUS_CHOICES = [

        ("OPEN","Open"),

        ("SOLVED","Solved"),

    ]


    pg = models.ForeignKey(
        PGProfile,
        on_delete=models.CASCADE
    )


    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )


    title = models.CharField(
        max_length=200
    )


    message = models.TextField()


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OPEN"
    )


    date = models.DateField(
        auto_now_add=True
    )


    def __str__(self):

        return self.title