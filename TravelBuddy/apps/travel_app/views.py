from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from time import localtime, strftime
import datetime
from django.utils.crypto import get_random_string

from .models import *
from ..login_app.models import *
import bcrypt
# Create your views here.
def index(request):
    #get trips of user_id
    logged_user = User.objects.get(id= request.session['user_data']['id'])
    trips_planned_by_logged_user = Trip.objects.filter(planned_by = logged_user)

    #get trips joined_by logged user:
    joined_by = Trip.objects.filter(joined_by = logged_user)
    print trips_planned_by_logged_user
    print type(trips_planned_by_logged_user)
    print joined_by
    print type(joined_by)
    records = (trips_planned_by_logged_user | joined_by).distinct()
    print records
    print type(records)

    #trips planned by other users
    trips_other_users = Trip.objects.exclude(planned_by = logged_user).exclude(joined_by = logged_user)
    print trips_other_users.values()
    others = trips_other_users.values('planned_by','planned_by__name','destination','description','travel_date_from','travel_date_to','id')


    context ={
    "records" : records,
    "others" :others
    }

    return render(request,'travel_app/index.html',context)

def add(request):
    return render(request,'travel_app/add.html')

def create_trip(request):
    #first get user_id from session
    errors = Trip.objects.data_validator_trip(request.POST)
    user_id = request.session['user_data']['id']
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/travels/add')
    else:
    #to be changed..
        planned_by_id = request.session['user_data']['id']
        user = User.objects.get(id=planned_by_id)
        from_date =  datetime.datetime.strptime( request.POST['from_date'], "%Y-%m-%d")
        to_date = datetime.datetime.strptime( request.POST['to_date'], "%Y-%m-%d")
        Trip.objects.create(destination = request.POST['destination'], description = request.POST['desc'], planned_by = user, travel_date_from=from_date, travel_date_to=to_date)
        print "trip created!"
        return redirect('/travels')

#method that shows trip details
def show(request, number):
    trip_id=number
    trip = Trip.objects.filter(id=trip_id)
    trip_values = trip.values('id','planned_by','planned_by__name','destination','description','travel_date_from','travel_date_to')
    print trip_values
    trip_values_other_users = trip.values('id','joined_by','joined_by__name')
    print trip_values_other_users
    context ={
        "trip" : trip_values,
        "others" : trip_values_other_users
    }
    return render(request, 'travel_app/trip.html',context)

def join(request,number):
    trip_id = number
    joined_by_id = request.session['user_data']['id']
    joined_by_user = User.objects.get(id = joined_by_id)
    trip = Trip.objects.get(id=trip_id)
    trip.joined_by.add(joined_by_user)
    trip.save()
    return redirect('/travels')

def logout(request):
    request.session.clear()
    return redirect('/main')
