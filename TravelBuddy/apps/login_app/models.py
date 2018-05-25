from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
# Create your models here.
EMAIL_REGEX =re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def checkUserNameAgainstDatabase(postData):
    user = User.objects.filter(username=postData['username'])
    if not user:
        return True
    else:
        return False
class UserManager(models.Manager):
    #function to check if email is already in database

    def data_validator_registration(self, postData):
        errors={}
        if len(postData['name']) < 1:
            errors['name'] = "Name cannot be blank!"
        elif len(postData['name']) < 3:
            errors['name'] = "Name cannot be less than 3 characters!"
        elif not postData['name'].replace(' ','').isalpha():
            errors['name'] = "Name cannot contain non-alphabets!"

        if len(postData['username']) < 1:
            errors['username'] = "Username cannot be blank!"
        elif len(postData['username']) < 3:
            errors['username'] = "Userame cannot be less than 2 characters!"


        #check if email already in database
        elif not checkUserNameAgainstDatabase(postData):
            errors['username'] = "Username already exists in database..!"

        if len(postData['password']) < 1:
            errors['password'] = "Password cannot be blank!"
        elif len(postData['password']) < 8:
            errors['password'] = "Password cannot be less than 8 characters!"

        if len(postData['pw_confirm']) < 1:
            errors['pw_confirm'] = "Enter Password again to confirm!"
        elif postData['password']!=postData['pw_confirm']:
            errors['pw_confirm'] = "Passwords do not match!"

        return errors

    def data_validator_login(self, postData):
        errors = {}
        if len(postData['username']) < 1:
            errors['username'] = "Please enter Username!"

        elif checkUserNameAgainstDatabase(postData):
            errors['username'] = "Username does not exist in our system!"

        if len(postData['password']) < 1:
            errors['password'] = "Password cannot be blank!"
        if not errors:
            # query db to check password
                user = User.objects.filter(username=postData['username'])
            # check input against hashed password
                hashed = user[0].password
                password = postData['password']
                if not bcrypt.checkpw(password.encode(), hashed.encode()):
                    errors['mismatch'] = "Incorrect password!!"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)

    objects = UserManager()
