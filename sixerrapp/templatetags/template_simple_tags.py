from django import template
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static

VERIFIED_BADGE_STATIC_IMAGE_PATH = static('img/verified.png')

register = template.Library()

# settings value
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")

@register.simple_tag()
def render_email_verified(profile):
    imgTag = ' <img src="' + VERIFIED_BADGE_STATIC_IMAGE_PATH + '">'
    if profile.vanitymail == settings.USER_EMAIL_PLACEHOLDER or not profile.emailverified:
        imgTag = ''
    return imgTag
