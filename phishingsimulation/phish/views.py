from django.shortcuts import render
from email.message import EmailMessage
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from phishingsimulation import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from .tokens import generate_token
import requests
from .email_logic import send_simulation_emails 


def index(request):
    return render(request, "index.html")
def home(request):
    return render(request,"home.html")
def signup(request):

    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if User.objects.filter(username=username):
            messages.error(request,"Username already exist! try any other Username")
            return redirect("signup")
        
        if User.objects.filter(email=email):
            messages.error(request,"Email ID already registered!")
            return redirect("signup")
        
        if len(username)>10:
            messages.error(request,"Username must be under 10 characters")
            return redirect("signup")
        
        if len(pass1)<8:
            messages.error(request,"Password must be 8 characters or more")
        
        if pass1 != pass2:
            messages.error(request,"Passwords didn't match!!")
            return redirect("signup")
        
        if not username.isalnum():
            messages.error(request,"Username must be Alpha-Numeric!!")
            return redirect("signup")
        

        myuser= User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active= False
        myuser.save()

        messages.success(request,"your account has been created successfully. we have sent you a confirmation,please confirm your email address to activate your account.")

        #welcome email
        subject ="Welcome to Phishing Simulation!"
        message ="Hello "+ myuser.first_name+" ,Welcome to Phishing Simulation, Welcome to Phishing Simulation, your go-to platform for simulating phishing attacks and enhancing your cybersecurity skills\n - Phishing Simulation"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        email_1=EmailMessage(subject,message,from_email,to_list)
        email_1.send()

        #confirmation email
        current_site =get_current_site(request)
        email_subject ="Confirm your email @ThreatHub - Login!!"
        message2= render_to_string('email_verification.html',{
                'name': myuser.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser)
                })
        email= EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently=True
        email.send()

    return render(request,"signup.html")
def signin(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST["username"]
        pass1 = request.POST["pass1"]

        user = authenticate(request ,username=username,password=pass1)
        if user is not None:
            login(request,user)
            fname =user.first_name
            lname =user.last_name
            return redirect("home")
        else:
            messages.error(request, "Wrong credentials!")
            return redirect("signin")


    return render(request,"signin.html")
def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode("utf-8")
        myuser= User.objects.get(pk=uid)
    except(TypeError, ValueError,OverflowError,User.DoesNotExist):
        myuser= None
    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        fname=myuser.first_name
        lname=myuser.last_name 
        return render(request,"home.html",{'fname':fname ,'lname': lname})
    else:
        return render(request,"verification_failed.html")
def logout_view(request):
    logout(request)
    return redirect("index")
def phishing(request):
    return render(request,"Phishing.html")
def simshing(request):
    return render(request,"simshing.html")
def SpearPhishing(request):
    return render(request,"SpearPhishing.html")
def Whaling(request):
    return render(request,"Whaling.html")

def trigger_simulation(request):
    if request.method == 'POST':
        user_email = request.POST["email"]
        username = "User"

        # Trigger the phishing and legitimate email simulation
        send_simulation_emails(request, user_email, username)

        # Display a success message after sending emails
        messages.success(request, 'Simulation emails sent successfully!')

        # Redirect to avoid duplicate submissions
        return redirect(trigger_simulation)

    return render(request, 'stimulate.html')
def fake_phishing_link(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Log the attempt, if necessary
        # You could log to a model or file here
        
        return HttpResponse("<h1>You have been hacked!</h1><p>It looks like you fell for a phishing attack.</p>")
    return render(request, 'fake_phishing.html')
def real_link(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # You could validate the credentials here if needed
        
        return HttpResponse("<h1>Congrats! You have become a human firewall!</h1><p>You successfully identified the correct link.</p>")
    return render(request, 'real_login.html')