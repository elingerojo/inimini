from .models import Profile
from django.contrib.staticfiles.templatetags.staticfiles import static
import random

def save_avatar(backend,user,response,*args,**kwargs):
    try:
        profile = Profile.objects.get(user_id=user.id)
    except Profile.DoesNotExist:
        profile = Profile(user_id=user.id)

    if backend.name == 'facebook':
        profile.avatar = 'https://graph.facebook.com/%s/picture?width=400&height=400 ' % response['id']
        if not profile.displayname:
            try:
                Profile.objects.get(displayname=user.username)
                user.username = user.username + str(random.randint(1,999999))
            except Exception as e:
                pass
            profile.displayname = user.username

        if profile.vanitymail == "replace.me@roast.gg":
            if user.email != None:
                profile.vanitymail = user.email

    profile.save()
