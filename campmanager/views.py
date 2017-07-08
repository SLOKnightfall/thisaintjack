import locale
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.cache import cache
from campmanager.models import Burner, Group, Area, SubCamp, CACHE_KEY
from django.shortcuts import render

def index(request):

    locale.setlocale(locale.LC_ALL, "")
    subcamps = SubCamp.objects.all().order_by('name')

    totalpeople = 0
    totalsqft = 0
    subcamp_list = []
    for subcamp in subcamps:
        subcamppeople = 0
        sites = Group.objects.filter(subcamp=subcamp)
        for site in sites:
            totalpeople += site.numpeople
            subcamppeople += site.numpeople

        sqft = int(subcamppeople) * 500
        totalsqft += sqft
        sqft = locale.format("%d", sqft, grouping=True)
        subcamp_list.append({ 'name' : subcamp.name,
                              'numpeople' : subcamppeople,
                              'sqft' : sqft,
                              'desc' : subcamp.desc })

    locale.setlocale(locale.LC_ALL, "")
    totalsqft = locale.format("%d", totalsqft, grouping=True)

    subcamps = SubCamp.objects.all().order_by('-name')
    sites = Group.objects.all().order_by('-numpeople')
    rvs = 0
    for site in sites:
        if site.type == 'r': rvs += 1
    rvssqft = 900 * rvs

    t = 'campmanager/index'
    c = {
        'subcamp_list': subcamp_list,
        'totalpeople' : totalpeople,
        'totalsubcamps' : len(subcamps),
        'totalsqft' : totalsqft,
        'rvs' : rvs,
        'rvssqft' : rvssqft,
    }
    return render(request, t, c)

types = { 't' : 'tent', 'o' : 'off-site', 'r' : "rv" }
def subcamp(request, subcamp):

    subcamps = SubCamp.objects.filter(name=subcamp)
    if not subcamps:
        err = "Camp %s does not exist!" % subcamp
        t = 'campmanager/error'
        c = {'err':err}
        return render(request, t, c)
    else:
        subcamp = subcamps[0]

    totalpeople = 0
    sites = Group.objects.filter(subcamp=subcamp)
    totalsites = len(sites)
    for site in sites:
        totalpeople += site.numpeople

    totalstuff = Area.objects.count()

    locale.setlocale(locale.LC_ALL, "")
    totalsqft = locale.format("%d", int(totalpeople) * 500, grouping=True)

    sites = Group.objects.filter(subcamp=subcamp).order_by('-numpeople')
    for site in sites:
        site.type = types[site.type] 
    t = 'campmanager/subcamp'
    c = {
        'subcamp' : subcamp,
        'site_list': sites,
        'totalpeople' : totalpeople,
        'totalsites' : totalsites,
        'totalstuff' : totalstuff,
        'totalsqft' : totalsqft,
    }
    return render(request, t, c)

def burnerlist(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login/?next=%s' % request.path)

    burners = Burner.objects.all().order_by('realname')
    t = 'campmanager/burners'
    c = {
        'burners': burners
    }
    return render(request, t, c)

def bigstufflist(request):

    bigstuff = Area.objects.all().order_by('-name')
    t = 'campmanager/bigstuff'
    c = {
        'bigstuffs': bigstuff
    }
    return render(request, t, c)
