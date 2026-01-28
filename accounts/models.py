from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
import os
from PIL import Image
from django.db.models.signals import post_save

# Create your models here.

def user_directory_path_profile(instance, filename):
    profile_picture_name = 'users/{0}/profile.jpg'.format(instance.user.username)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_name


def user_directory_path_banner(instance, filename):
    profile_picture_name = 'users/{0}/banner.jpg'.format(instance.user.username)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_name


VERIFICATION_OPTIONS=(
    ('unverified', 'unverified'),
    ('verified', 'verified'),
)


class User(AbstractUser):
    stripe_customer_id = models.CharField(max_length=50)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    picture = models.ImageField(default='users/user_default_profile.png', upload_to=user_directory_path_profile)
    banner = models.ImageField(default='users/user_default_bg.jpg', upload_to=user_directory_path_banner)

    verified = models.CharField(max_length=10, choices=VERIFICATION_OPTIONS, default='unverified')

    coins = models.DecimalField(max_digits=19, decimal_places=2, default=0, blank=False)

    followers = models.ManyToManyField(User, blank=True, related_name="followers")

    date_created = models.DateField(auto_now_add=True)

    #User info
    location = models.CharField(max_length=50, blank=True)
    url = models.CharField(max_length=80, blank=True)
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=150,  blank=True)

    zone = models.ForeignKey(
        "ads.Zone",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# created profile
post_save.connect(create_user_profile, sender=User)
# save created profile
post_save.connect(save_user_profile, sender=User)

class UserOpinion(models.Model):
    profile = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.CASCADE,
        related_name="opinions",
        null=True,   # 👈 TEMPORAL
        blank=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="given_opinions"
    )
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "author"],
                name="one_opinion_per_user_per_profile"
            )
        ]

    def __str__(self):
        return f"{self.author} → {self.profile}"
