from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Gig
from sixerrapp import forms
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_GET, require_POST

# validate_email
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
import re
import requests


# Create bot user but NOT when running "makemigrations" because ...
# ... "auth_user" table has not been created and causes "OperationalError"
try:
    BOT_USER, created = User.objects.get_or_create(username='bot', \
                                                        email=settings.EMAIL_HOST_USER)
# Catch any error
except:
    created = False

if created:
    BOT_USER.set_password(settings.EMAIL_HOST_PASSWORD)
    BOT_USER.save()

    try:
        profile = Profile.objects.get(user_id=BOT_USER.id)
    except Profile.DoesNotExist:
        profile = Profile(user_id=BOT_USER.id)

    profile.displayname = 'Roasty'
    profile.avatar = static('img/logo.png')
    profile.save()

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def overview(request):
    # Render plain html overview page
    return render(request, 'overview.html')

def termsofuse(request):
    return render(request,'termsofuse.html')

def privacypolicy(request):
    return render(request,'privacypolicy.html')

@login_required(login_url="/")
def create_gig(request):
    error = ''

    if request.method == 'POST':
        gig_form = forms.GigForm(request.POST, request.FILES)
        if gig_form.is_valid():
            gig = gig_form.save(commit=False)
            gig.user = request.user
            gig.save()
            return redirect('my_gigs')
        else:
#            error = "Data is not valid"
            error = gig_form.errors

    gig_form = forms.GigForm()

    return render(request, 'create_gig.html',{"error":error})

@require_POST
@login_required(login_url="/")
def delete_gig(request, id):
    error = ''
    try:
        gig = Gig.objects.get(id=id,user=request.user)
        gig.delete()
    except Exception as e:
        error = 'Gig to delete not found'

    gigs = Gig.objects.filter(user=request.user)
    return render(request, 'my_gigs.html',{"gigs":gigs, "error": error})

@login_required(login_url="/")
def my_gigs(request):
    try:
        profile = Profile.objects.get(user = request.user)
    except Profile.DoesNotExist:
        return redirect('/')

    gigs = Gig.objects.filter(user=request.user)
    return render(request, 'my_gigs.html',{"gigs":gigs})

@login_required(login_url="/")
def edit_gig(request, id):
    try:
        error = ''
        gig = Gig.objects.get(id=id,user=request.user)
        if request.method == "POST":
            print('POST = ', request.POST)
            gig_form = forms.GigForm(request.POST,request.FILES, instance=gig)
            if gig_form.is_valid():
                gig.save()
                return redirect('my_gigs')
            else:
                error = "Data is not valid"

        return render(request, 'edit_gig.html', {"gig":gig ,
                                                "error":error})

    except Gig.DoesNotExist:
        return redirect('/')

def profile(request, username):
    try:
        profile = Profile.objects.get(displayname = username)
    except Profile.DoesNotExist:
        return redirect('/')

    postError = ''
    if request.method == "POST" and 'profile_form' in request.POST:
        profile_form = forms.ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile.save()
        else:
            postError = "Data is not valid"

    if request.method == "POST" and 'emailvalidate_form' in request.POST:
        vanitymail = request.POST['vanitymail'] if 'vanitymail' in request.POST else 'noEmail'
        confirm_vanitymail = request.POST['confirm_vanitymail'] if 'confirm_vanitymail' in request.POST else 'noConfiramtion'
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', vanitymail)

        if match and vanitymail == confirm_vanitymail:

            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            # TODO: Change captcha synchronous hanndling to asynchronous
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' End reCAPTCHA validation '''

            if result['success']:

                profile.vanitymail = vanitymail
                profile.emailverified = False
                profile.save()
                # Verify email message template
                msg =       'Hello {username},\n'
                msg = msg + 'Please click on the link to confirm your registration.\n'
                msg = msg + settings.HOST_URL + '/validate_email/' +'{uidb64}/{token}\n'
                msg = msg + '\n'
                msg = msg + signature(username)

                # Fill message template
                msg = msg.format(username = username,
                                uidb64 = urlsafe_base64_encode(force_bytes(profile.user.pk)).decode('ascii'),
                                token = account_activation_token.make_token(profile.user) )

                send_mail('Verify your email for Roast.gg',     # subject
                        msg,                                    # content
                        settings.EMAIL_HOST_USER,               # from
                        [vanitymail],                           # to
                        fail_silently=False)
                return redirect('profile', username = username)
            else:
                # It is a Robot
                return redirect('home')
        else:
            postError = "Email or Confiramtion error"

    return render(request, 'profile.html', {"profile":profile, "postError": postError})

@require_GET
@csrf_exempt
def validate_email(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and profile is not None and account_activation_token.check_token(user, token):
        user.profile.emailverified = True
        user.profile.save()
        message = """
Thank you for your email confirmation.
Now you can receive messages from us according to your notification preferences.
"""
        # return redirect('home')
        return render(request, 'standAloneTemplates/thankyou.html', {"message": message})
    else:
        return HttpResponse('Activation link is invalid!')

def signature(profile_username):
    return """
- The Roast.gg team

Notice: You are receiving this email per your request as part of our Terms of Use.
You can change your email preferences by log in and editing your profile in the following link:
""" + settings.HOST_URL + "/profile/" + str(profile_username) + "/" + """

Do not reply. The notifications email is not monitored.

If you are receiving this email in error, please contact us at contact.us@roast.gg so we can correct it immediately.
"""
