from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from random import randint
# Create your views here.

default_data = {}

def Index_page(request):
    if 'email' in request.session:
        # profile_data(request) # load profile data
        return render(request, 'index.html')
    else:
        return redirect(Signin_page)

def Signin_page(request):
    return render(request,"signin.html")

def Signup_page(request):
    return render(request,"signup.html")

def Forgot_password(request):
    return render(request,"sign_up.html")

def otp_page(request):
    return render(request,"otp.html")

def My_profile(request):
    return render(request, "my_profile.html")

def My_orders(request):
    return render(request, "my_orders.html")

def My_wishlist(request):
    return render(request, "my_wishlist.html")

def My_addresses(request):
    return render(request, "my_addresses.html")

def Changepass_page(request):
    return render(request, "change_password.html")

def Aboutus_page(request):
    return render(request,"about_us.html")

def Shopgrid_page(request):
    return render(request,"shopgrid.html")

def Contactus_page(request):
    return render(request,"contact_us.html")

def Checkout_page(request):
    return render(request,"checkout.html")





# Signup Functionality
def Signup(request):
    if request.POST['password'] == request.POST['cpassword']:
        try:
            Master.objects.get(Email=request.POST['email'])
            messages.error(request, "User Already Exist.")
            return render(request,'signup.html')

        except Master.DoesNotExist:
            master = Master.objects.create(Email=request.POST['email'],Password=request.POST['password'])
            UserProfile.objects.create(Master=master)
            messages.success(request, "User Sign Up Successfully.")
            return redirect(Signin_page)
            # return render(request,'index.html')

    else:
        messages.error(request, "Both Password Should Be Same.")
        return redirect(Signup_page)


# Signin Functionality
def Signin(request):
    try:
        master = Master.objects.get(Email = request.POST['email'])
        if master.Password == request.POST['password']:
            request.session['email'] = master.Email
            messages.success(request, "Welcome to GrossyFy.")
            return redirect(Index_page)
        else:
            messages.success(request, "Password Does Not Match.")
            return render(request,"signin.html")
        
    except Master.DoesNotExist:
        messages.error(request, "User Does Not Exist.")
        return render(request,"signin.html")

# Signout Functionality
def Signout(request):
    if 'email' in request.session:
        del request.session['email']
        messages.success(request, "User Sign Out Successfully.")
        return redirect(Signin_page)
    return redirect(Index_page)



# Update Profile 
def Profile_update(request):
    master = Master.objects.get(Email = request.session['email'])
    user_profile = UserProfile.objects.get(Master = master)
    user_profile.Firstname = request.POST['firstname']
    user_profile.Lastname = request.POST['lastname']
    user_profile.Contact = request.POST['contact']
    user_profile.BirthDate = request.POST['birthdate']
    user_profile.Gender = request.POST['gender']
    user_profile.City = request.POST['city']
    user_profile.State = request.POST['state']
    user_profile.Pincode = request.POST['pincode']

    user_profile.save()

    return redirect(my_profile)

def Add_address(request):
    master = Master.objects.get(Email=request.session['email'])
    address = UserProfile.objects.get(Master = master)
    address.HomeAddress = request.POST['home_address']
    address.OfficeAddress = request.POST['office_address']
    address.OtherAddress = request.POST['other_Address']

    address.save()
    return redirect(My_addresses)

#Load Profile data

# def Profile_data(request):
#     master = Master.objects.get(Email = request.POST['email'])
#     user_profile = UserProfile.objects.get(Master = master)
#     user_profile.email = Master.Email

def profile_data(request):
    master = Master.objects.get(Email = request.session['email'])
    user_profile = UserProfile.objects.get(Master = master)
    user_profile.first_name = user_profile.Firstname
    user_profile.last_name = user_profile.Lastname

    default_data['user_data'] = user_profile


# Change Password Functionlity
def Changepass(request):
    master = Master.objects.get(Email=request.session['email'])
    if master.Password == request.POST['current_password']:
        if request.POST['new_password'] == request.POST['confirm_password']:
            master.Password = request.POST['new_password']
            master.save()
            messages.success(request, "password Changed Successfully.")
            return redirect(Changepass_page)
        else:
            messages.error(request, "Current Password & New Password Does Not Match.")
            return redirect(Changepass_page)


    return redirect(Changepass_page)


# OTP Creation
def Create_otp(request):
    otp_number = randint(100000, 999999)
    request.session['otp'] = otp_number


# send_otp
def send_otp(request, otp_for="register"):
    print(otp_for)
    otp(request)

    email_to_list = [request.session['reg_data']['email'],]

    if otp_for == 'activate':
        request.session['otp_for'] = 'activate'
        subject = f'OTP for Budget Account Activation'
    elif otp_for == 'recover_pwd':
        request.session['otp_for'] = 'recover_pwd'
        subject = f'OTP for Budget Password Recovery'
    else:
        request.session['otp_for'] = 'register'
        subject = f'OTP for Budget Registration'

    email_from = settings.EMAIL_HOST_USER

    message = f"Your One Time Password for verification is: {request.session['otp']}."

    send_mail(subject, message, email_from, email_to_list)


# verify otp
def verify_otp(request, verify_for="register"):

    if request.session['otp'] == int(request.POST['otp']):

        if verify_for == 'activate':
            master = Master.objects.get(Email=request.session['reg_data']['email'])
            # master.Password = request.session['reg_data']['password']
            master.IsActive = True
            master.save()


            return redirect(profile_page)
        elif verify_for == 'recover_pwd':
            master = Master.objects.get(Email=request.session['reg_data']['email'])
            master.Password = request.session['reg_data']['password']
            master.save()
        else:
            print('before new account')
            master = Master.objects.create(
                Email = request.session['reg_data']['email'],
                Password = request.session['reg_data']['password'],
                IsActive = True,
            )

            UserProfile.objects.create(
                Master = master,
            )
            print('after new account')

        print("verified.")
        del request.session['reg_data']

    else:
        print("Invalid OTP")
        
        return redirect(otp_page)
    
    return redirect(Signin_page)


