from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from time import localtime, strftime
from datetime import datetime
from django.utils.crypto import get_random_string

from .models import User
import bcrypt

# Create your views here.
def index(request):
    return render(request,'login_app/index.html')

def register(request):
    errors = User.objects.data_validator_registration(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/main')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hashed_pw)
        inserted_user = User.objects.last()
        id = inserted_user.id
        request.session['user_data']={
        "id" : id,
        "name":request.POST['name'],
        "username" : request.POST['username']
        }
        request.session['type'] = 'registered'

        return redirect('/travels')
def login(request):
    errors = User.objects.data_validator_login(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/main')
    else:
        user = User.objects.filter(username=request.POST['username'])
        request.session['user_data']={
        "id" : user[0].id,
        "name":user[0].name,
        "username" : user[0].username
        }
        request.session['type'] = 'logged in'
        return redirect('/travels')
