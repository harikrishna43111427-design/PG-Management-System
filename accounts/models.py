from django.db import models
from django.contrib.auth.models import User



class PGProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )


    pg_id = models.CharField(
        max_length=10,
        unique=True,
        blank=True
    )


    profile_image = models.ImageField(
        upload_to="profile_images/",
        default="profile_images/default.png",
        blank=True
    )


    pg_name = models.CharField(
        max_length=100
    )


    branch = models.CharField(
        max_length=100
    )


    address = models.TextField()


    phone = models.CharField(
        max_length=15
    )


    capacity = models.IntegerField(
        default=0
    )


    def save(self, *args, **kwargs):

        if not self.pg_id:

            last_pg = PGProfile.objects.order_by(
                "-id"
            ).first()


            if last_pg:

                number = last_pg.id + 1

            else:

                number = 1


            self.pg_id = f"PG{number:04d}"


        super().save(*args, **kwargs)



    def __str__(self):

        return self.pg_name





class PasswordOTP(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    otp = models.CharField(
        max_length=6
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return self.user.username
class PasswordOTP(models.Model):
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    otp = models.CharField(
        max_length=6
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return self.user.username