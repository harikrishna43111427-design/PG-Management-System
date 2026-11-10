from django.urls import path


from . import views


urlpatterns = [
    path(
        "register/",
        views.register,
        name="register"
    ),
     path(
        "",
        views.login,
        name="login"
    ),
      path(
        "owner-dashboard/",
        views.owner_dashboard,
        name="owner_dashboard"
    ),
    path(
    "profile/",
    views.profile,
    name="profile"
   ),
    path(
    "edit-profile/",
    views.edit_profile,
    name="edit_profile"
),
    path(
    "logout/",
    views.user_logout,
    name="logout"
),
    path(
    "forgot-password/",
    views.forgot_password,
    name="forgot_password"
),
    path(
    "reset-password/",
    views.reset_password,
    name="reset_password"
),
    path(
    "verify-otp/",
    views.verify_otp,
    name="verify_otp"
),
    

]