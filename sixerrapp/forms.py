from django.forms import ModelForm, ValidationError
from .models import Profile, Gig
# from django.core.exceptions import ValidationError
from django.conf import settings
import re

# *******************
# Initialization code
# TODO: Find a better place for this code
# *******************

# ... any initialization code goes here
available_select_options = {}

# **************************
# End of initialization code
# ... continue with Forms
# *************************

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['displayname', 'about', 'slogan', 'emailoptin']

class EmailVerifyForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['vanitymail', 'emailverified']

class GigForm(ModelForm):
    class Meta:
        model = Gig
        fields = ['title', 'category', 'description', 'price', 'photo', 'status']

    # Validation for 'photo' field
    def clean_photo(self):
        data = self.cleaned_data['photo']

        # If empty, inject fixed placeholder image
        if not data:
            data = settings.MEDIA_PLACEHOLDER_IMAGE_PATH

        # Remember to always return the cleaned data.
        return data
