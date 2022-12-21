from django.urls import path
from .views import *

urlpatterns = [
    path('Index_page/', Index_page, name='Index_page'),
    path('', Signin_page, name='Signin_page'),
    path('Signup_page/', Signup_page, name='Signup_page'),
    path('otp_page/', otp_page, name='otp_page'),
    path('My_addresses/', My_addresses, name='My_addresses'),
    path('My_orders/', My_orders, name='My_orders'),
    path('My_profile/', My_profile, name='My_profile'),
    path('My_wishlist/', My_wishlist, name='My_wishlist'),
    path('Changepass_page/', Changepass_page, name='Changepass_page'),
    path('Aboutus_page/', Aboutus_page, name='Aboutus_page'),
    path('Shopgrid_page/', Shopgrid_page, name='Shopgrid_page'),


    path('Signup/',Signup, name='Signup'),
    path("Signin/", Signin, name="Signin"),
    path('Signout/', Signout, name='Signout'),
    path("Profile_update/", Profile_update, name="Profile_update"),
    path("Changepass/", Changepass, name="Changepass"),
]
