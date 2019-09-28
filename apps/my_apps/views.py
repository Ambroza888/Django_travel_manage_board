from django.shortcuts import render, HttpResponse, redirect
from .models import *
import bcrypt
from django.contrib import messages


def index(request):
    return render(request, "my_apps/index.html")


def reg_in_data(request):
  errors = User.objects.basic_validator(request.POST)
  if len(errors) > 0:
    for key, value in errors.items():
      # messages.error(request, value)
      messages.add_message(request, messages.ERROR, value, extra_tags="register")
    return redirect('/')
  else:
    name = request.POST['name']
    alias = request.POST['alias']
    email = request.POST['email']
    password = request.POST['password']
    re_password = request.POST['re_password']
    pw_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
    new_user = User.objects.create(name=name,alias=alias,email=email,password=pw_hash)
    id = new_user.id
    request.session['user_id'] = id

    return redirect("/dashboard")

def log_in_data(request):
  user = User.objects.filter(email=request.POST['email'])
  if user:
    logged_user = user[0]
    if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
      request.session['user_id'] = logged_user.id
      return redirect("/dashboard")
    else:
      messages.add_message(request, messages.ERROR, "Invalid information", extra_tags='login')
      return redirect('/')
  else:
    return redirect('/')

def clean_session(request):
  request.session.clear()
  return redirect('/')

def dashboard(request):
  if not "user_id" in request.session:
    return redirect('/')
  user = User.objects.get(id=int(request.session['user_id']))
  context = {
    "chosen_user_trips": Trip.objects.filter(user=user),
    "all_trips":Trip.objects.exclude(user=user),
    "the_user": user
  }
  return render(request, "my_apps/dashboard.html",context)



def trips_info(request,my_val):
  if not "user_id" in request.session:
    return redirect("/")
  else:
    context = {
        "chosen_trip": Trip.objects.get(id=int(my_val)),
        "the_user": User.objects.get(id=request.session['user_id'])
  }

  return render(request, "my_apps/trips_info.html",context)

def create_trip(request):
  if not "user_id" in request.session:
    return redirect('/')
  else:
    context = {
      "user": User.objects.get(id=int(request.session['user_id']))
    }
  return render(request, "my_apps/create_trip.html",context)


def work_on_trip(request):
  errors = Trip.objects.basic_validator_trip(request.POST)
  if len(errors) > 0:
    for key,value in errors.items():
      messages.error(request, value)
    return redirect('/create_trip')
  else:
    user = User.objects.get(id=int(request.session['user_id']))
    dest = request.POST['destination']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    plan = request.POST['plan']
    new_trip = Trip.objects.create(destination=dest,start_date=start_date,end_date=end_date,plan=plan,user=user)
    return redirect('/dashboard')

def remove_trip(request,my_val):
  trip = Trip.objects.get(id=int(my_val))
  trip.delete()
  return redirect('/dashboard')


def edit_trip(request,my_val):
  if not "user_id" in request.session:
    return redirect('/')
  else:
    context = {
      "user": User.objects.get(id=int(request.session['user_id'])),
      "trip":Trip.objects.get(id=int(my_val))
    }

    return render(request, "my_apps/edit_trip.html",context)

def update_trip(request,my_val):
  errors = Trip.objects.basic_validator_edit_trip(request.POST)
  if len(errors) > 0:
    for key,value in errors.items():
      messages.error(request, value)
    return redirect(f'/edit_trip/{my_val}')
  else:
    dest = request.POST['dest']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    plan = request.POST['plan']
    trip = Trip.objects.get(id=int(my_val))
    trip.destination = dest
    trip.start_date = start_date
    trip.end_date = end_date
    trip.plan = plan
    trip.save()
    return redirect('/dashboard')