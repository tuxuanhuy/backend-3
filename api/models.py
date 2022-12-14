from django.db import models
from django.contrib.auth.models import AbstractUser

from PIL import Image
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile

import cv2
import os

# Create your models here.

def user_path(instance, filename):
    return '{0}/{1}'.format(instance.user.username, filename)


class User(AbstractUser):
    first_name   = models.CharField(max_length=100)
    last_name    = models.CharField(max_length=100)
    email        = models.CharField(max_length=100)
    address      = models.CharField(max_length=100)
    contact      = models.CharField(max_length=100)
    
    username     = models.CharField(max_length=100, unique=True)
    password     = models.CharField(max_length=100, default=1)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.username
        
    class Meta:
        db_table = 'users'


class Face(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    picture      = models.ImageField(upload_to=user_path, max_length=255, null=True, blank=True)

    def get_picture(self):
        if self.picture:
            return 'http://127.0.0.1:8000' + self.picture.url
        return ''

    def __str__(self):
        return "{}".format(self.user.username)

    def save(self, *args, **kwargs):

        pil_img = Image.open(self.picture)

        cv_img = np.array(pil_img)
        img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

        im_pil = Image.fromarray(img)

        buffer = BytesIO()
        im_pil.save(buffer, format='png')
        image_png = buffer.getvalue()

        self.picture.save(str(self.picture), ContentFile(image_png), save=False)

        super().save(*args, **kwargs)



class Shift(models.Model):
    name         = models.CharField(max_length=100)
    start_time   = models.TimeField(default=None)
    end_time     = models.TimeField(default=None)
    status       = models.BooleanField(default=True)
    date         = models.DateField(default=None)

    user         = models.ForeignKey(User, on_delete=models.CASCADE, default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'shift'
