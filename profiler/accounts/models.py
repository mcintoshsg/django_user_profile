''' database models for the accounts application '''

import datetime

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ''' user profile model, which extends the User model from Django '''
    user = models.OneToOneField(User)
    date_of_birth = models.DateField(default=datetime.datetime.now().strftime(
        '%d/%m/%Y'), blank=True, null=True)
    bio = models.CharField(max_length=300, blank=True)
    avatar = models.ImageField(
        upload_to='avatar_imgs/', blank=True)

    def __str__(self):
        return self.user.username
