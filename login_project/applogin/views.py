from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth,sessions
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template import TemplateSyntaxError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from . tokens import generate_token
import logging
from login_project import settings
logger = logging.getLogger('django')

# Create your views here.

# starting our login system confirgrations
def home(request):
    return render(request, "index.html")

# signup for login system
def signup(request):
    # print('signup: ', request.method)
    if(request.method == "POST"):
        # username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "username already exist! please try some other username")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, 'Email is already registered')
            return redirect('home')

        if len(username) > 10:
            messages.error(request, 'username must be under 10 character')

        if password != confirm_password:
            messages.error(request, 'Passwords did not match')

        # if not username.isalnum():
        #     messages.error(request,"username must be Alpha-numeric")
        #     return redirect('home')

        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        # print(email)
        #messages.success(request, 'Your Account has been successfully created. we have sent you a confirmation email, please confirm your eamail in order to activate your account.')

        # subject = "Welcome to login_system_project"
        # message = "Hello" + myuser.first_name + "!! \n" +"Welcome to login_system!!\n Thank you for visiting our website \n we have also sent you a confirmation email, please confirm your email address in order to activate your account \n Thanking You \n Amit jain"
        # from_email = settings.EMAIL_USER
        # to_list = [myuser.email]
        # send_mail(subject,message,from_email,to_list,fail_silently=True )

        # send mail request for authentication mail for login functionality
        subject = "Greetings from shubham"
        msg = "you are successfully registered"
        to = email
        send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])

        current_site = get_current_site(request)
        email_subject = "Confirm your email @ login_system_project - Django login!!"
        message2 = render_to_string("email_confirmation.html", {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return render(request,"authentication.html")

    return render(request, "signup.html")

# for login account
def login_user(request):
    logger.debug('some message')
    print('req method: ', request.method)
    # print('login')
    if(request.method == "POST"):
        username = request.POST['username']
        #print("Username", username)
        password= request.POST['pass1']
        #print("password", password)
        
        user = authenticate(request, username=username, password=password)
        print('user: ', user)
        if user is not None:
            logger.debug('special message')
            print("inside user: ", user)
            auth.login(request, user)
            #fname = user.first_name
            #return render(request, "index.html", {'fname': fname})
            #return HttpResponseRedirect('index')
            return redirect('/')
        else:
            messages.error(request, "Bad credentials")
            logger.info("very important")
            return redirect('home')

    return render(request, "login.html")

#for logout our account
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')

#for activation our account
def activate(request, uid64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, TemplateSyntaxError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        # login(request, myuser)
        return redirect('home')
    else:
        return render(request, "activation_failed.html")

# maintain our sessions
def setsession(request):
    request.session['username'] = request.POST['username']
    request.session['password'] = request.POST['pass1']
    return render("login")

# maintain our sessions
def getsession(request):
    request.session['username'] = request.POST['username']
    request.session['password'] = request.POST['pass1']
    return render('login')
