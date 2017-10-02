from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator

# Create your models here.

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayname = models.CharField(max_length=150, null=True,blank=True, unique=True)
    avatar = models.CharField(max_length=500)
    about = models.TextField(max_length=2000, blank=True, null=True)
    slogan = models.CharField(max_length=500, blank = True, null=True)
    vanitymail = models.CharField(max_length=128, default="replace.me@roast.gg")
    emailoptin = models.BooleanField(default=True)
    emailverified = models.BooleanField(default=True)

    def __str__ (self):
        return self.user.username

class Gig(models.Model):
    CATEGORY_CHOICES = (
            ("LL", "League of Legends"),
            ("OW", "Overwatch")
        )
    MAX_GIG_PRICE = 500
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.ForeignKey(User)
    create_time = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=500, validators=[MinLengthValidator(2,"length less than two")])
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    description = models.TextField(max_length=2000, validators=[MinLengthValidator(2,"length less than two")])
    price = models.IntegerField(default=6, validators=[ \
                    MinValueValidator(1,"minimum allowable $1"), \
                    MaxValueValidator(MAX_GIG_PRICE,"more than max allowable price")])
    photo=models.CharField(max_length=250, blank=True) # clean_photo() injects placeholder
    status = models.BooleanField(default=True)

    def __str__ (self):
        return self.title
