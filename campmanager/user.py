from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django import forms as forms
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.core.cache import cache
from campmanager.models import Burner, Group, CACHE_KEY
from campmanager.forms import SignUpForm, MyProfileForm
from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash
import datetime

def login(request):
    return render_to_response("campmanager/user/login")

def login_created(request):
    return render_to_response("campmanager/user/login_created")

def login_error(request):
    error = request.GET.get('error', 'Unknown!')
    return render_to_response("campmanager/user/login_error", {
        'error' : error
    })

def disconnected(request):
    logout(request)
    return HttpResponseRedirect("/")

def newlogin(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            burner = Burner()
            burner.user = new_user
            burner.arrival_date = "2012-10-13"
            burner.email = form.cleaned_data.get('email')
            burner.realname = form.cleaned_data.get('username')
            burner.save()
            cache.delete(CACHE_KEY)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user: auth_login(request, user)
            return HttpResponseRedirect("/user/profile")

    else:
        form = SignUpForm()
    return render(request, 'campmanager/user/newlogin', {'form': form})

def logoff(request):
    logout(request)
    return HttpResponseRedirect("/")

def myprofile(request):

    setup = request.GET.get('setup', '')
    msg = None
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login/?next=%s' % request.path)

    burnerList = Burner.objects.filter(user=request.user.id)
    user = User.objects.get(username = request.user)
    if burnerList:
        burner = burnerList[0]
    else:
        burner = Burner(user=request.user)

    if request.method == 'POST':
        if 'A' in request.POST:
            form = MyProfileForm(request.POST, user=request.user)
            pw_form = PasswordChangeForm(request.user)

            if form.is_valid():
                burner.realname = form.cleaned_data.get('username')
                user.username = form.cleaned_data.get('username')
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.email = form.cleaned_data.get('email')
                burner.email = form.cleaned_data.get('email')
                burner.mobile = form.cleaned_data.get('phone')
                burner.arrival_date = "2012-10-13"
                msg = "Profile saved."
                burner.save()
                user.save()
        if 'B' in request.POST:
            form = MyProfileForm(initial={'username': user.username,
                                            'first_name':user.first_name,
                                            'last_name':user.last_name,
                                            'email':user.email,
                                            'phone':burner.mobile})
            pw_form = PasswordChangeForm(request.user, request.POST)

            if pw_form.is_valid():
                user = pw_form.save()
                update_session_auth_hash(request, user)  # Important!
                msg = 'Your password was successfully updated!'
    #        try:
    #            burner.arrival_date = datetime.datetime.strptime(request.POST['arrival_date'], "%m-%d-%Y") #.strftime("%Y-%m-%d")
    #            msg = "Profile saved."
    #            burner.save()
    #        except ValueError:
    #            msg = "Invalid arrival date. Please format mm-dd-yyyy."
    #            burner.arrival_date = datetime.date.today()
            #if request.POST['setup'] == '1':
            #    return HttpResponseRedirect('/group/0/?setup=1')
    else:
        form = MyProfileForm(initial={'username': user.username,
                                        'first_name':user.first_name,
                                        'last_name':user.last_name,
                                        'email':user.email,
                                        'phone':burner.mobile})

        pw_form = PasswordChangeForm(request.user)
    t = 'campmanager/user/myprofile'
    c = {  'msg' : msg,
            'realname' : burner.realname,
            'first_name':burner.user.first_name,
            'last_name':burner.user.last_name,
            'phone' : burner.mobile,
            'email': burner.email,
            'setup' : setup,
            'form': form,
            'pw_form':pw_form,
#            'arrival_date' : str(burner.arrival_date) or "",
#            'arrival_date_y' : burner.arrival_date.year,
#            'arrival_date_m' : burner.arrival_date.month,
#            'arrival_date_d' : burner.arrival_date.day,
        }
    return render(request, t, c)

def profile(request, username):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login/?next=%s' % request.path)

    u = User.objects.get(username__exact=username)
    if u:
        burnerList = Burner.objects.filter(user=u.id)
        if burnerList:
            burner = burnerList[0]
        else:
            burner = None
    else:
        c =  {  'burner' : username,
                'error' : "No such user, doofus!" }
        return render(request, t, c)

    groups = Group.objects.filter(user=u.id)
    t = 'campmanager/user/profile'
    if burner:
        c = {   'burner' : username,
                'realname' : burner.user.first_name + " " +burner.user.last_name,
                'phone' : burner.mobile,
                'arrival_date' : burner.arrival_date,
                'email' : burner.user.email,
		        'groups' : groups,
        }
    else:
        c = {   'burner' : u.username,
                'realname' : u.first_name + " " + u.last_name,
                'phone' : '',
                'arrival_date' : '',
                'email' : u.email,
		        'groups' : groups, }
    return render(request, t, c)

def help(request):
    t = 'campmanager/user/help'
    c = {}
    return render(request, t, c)
