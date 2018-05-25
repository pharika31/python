from __future__ import unicode_literals

from django.db import models
from ..login_app.models import User
import time
import datetime
import re
import bcrypt

class TripManager(models.Manager):

    def data_validator_trip(self,postData):
        errors={}
        if len(postData['destination']) < 1:
            errors['destination'] = "Destination cannot be blank!"
        elif len(postData['destination']) < 2:
            errors['destination'] = "Destination cannot be less than 2 characters!"
        elif not postData['destination'].replace(' ','').isalpha():
            errors['destination'] = "Destination cannot contain non alphabets!"

        if len(postData['desc']) < 1:
            errors['desc'] = "Description cannot be blank!"
        elif len(postData['desc']) < 2:
            errors['desc'] = "Description cannot be less than 2 characters!"
        #to add date validations
        if len(postData['from_date']) < 1:
            errors['from_date'] = "Enter valid date in mm/dd/yyyy format!"
        if len(postData['to_date']) < 1:
            errors['to_date'] = "Enter valid date in mm/dd/yyyy format!"

        else:

            from_date = datetime.datetime.strptime(postData['from_date'], "%Y-%m-%d")
            to_date = datetime.datetime.strptime(postData['to_date'], "%Y-%m-%d")
            current_date_as_string = datetime.datetime.now().strftime("%Y-%m-%d")
            current_date = datetime.datetime.strptime(current_date_as_string,"%Y-%m-%d")
            print current_date
            if current_date > from_date:
                errors['from_date'] = "From date cannot be in the past!!"

            if to_date < from_date:
                errors['to_date'] = "To Date cannot be less than From date"

        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    travel_date_from = models.DateTimeField()
    travel_date_to = models.DateTimeField()
    planned_by = models.ForeignKey(User)
    joined_by = models.ManyToManyField(User, related_name='trips')#one user can join multiple trips

    objects = TripManager()
