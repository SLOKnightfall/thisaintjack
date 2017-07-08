from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django import forms as forms
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, logout, login
from django.core.cache import cache
from campmanager.models import Burner, Group, CACHE_KEY
from django.shortcuts import render
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
    form = UserCreationForm()
    if request.method == 'POST':
        data = request.POST.copy()
        errors = form.get_validation_errors(data)
        if not errors:
            if data['magicword'] == "bacon":
		new_user = form.save(data)
		burner = Burner()
		burner.user = new_user
		burner.save()
		cache.delete(CACHE_KEY)
		user = authenticate(username=data['username'], password=data['password1'])
		if user: login(request, user)
		return HttpResponseRedirect("/user/profile")
            else:
                # this is a total cheat, but doing this without an entry in the model is a pita
                data['badmagicword'] = "1"

    else:
        data, errors = {}, {}
        try:
            del data['badmagicword']
        except KeyError:
            pass

    return render_to_response("campmanager/user/newlogin", {
        'form' : forms.FormWrapper(form, data, errors)
    })

def logoff(request):
    logout(request)
    return HttpResponseRedirect("/")

def myprofile(request):

    setup = request.GET.get('setup', '')
    msg = None
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login/?next=%s' % request.path)

    burnerList = Burner.objects.filter(user=request.user.id)
    if burnerList: 
        burner = burnerList[0]
    else:
        burner = Burner(user=request.user)

    if request.method == 'POST':
        burner.realname = request.POST['realname'] 
        burner.mobile = request.POST['phone']
        burner.arrival_date = "2012-10-13"
        msg = "Profile saved."
        burner.save()

#        try:
#            burner.arrival_date = datetime.datetime.strptime(request.POST['arrival_date'], "%m-%d-%Y") #.strftime("%Y-%m-%d")
#            msg = "Profile saved."
#            burner.save()
#        except ValueError:
#            msg = "Invalid arrival date. Please format mm-dd-yyyy."
#            burner.arrival_date = datetime.date.today()
        if request.POST['setup'] == '1':
            return HttpResponseRedirect('/group/0/?setup=1')

    t = 'campmanager/user/myprofile'
    c = {  'msg' : msg,
            'realname' : burner.realname,
            'phone' : burner.mobile,
            'setup' : setup,
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
                'realname' : burner.realname,
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

