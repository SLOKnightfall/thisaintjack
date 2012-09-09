from django.db import models
from django.contrib.auth.models import User

CACHE_KEY = 'taj_stats'

# Create your models here.
class Burner(models.Model):
    user = models.ForeignKey(User)
    print user.name
    realname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    mobile = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % self.realname

    class Admin:
        pass

class SubCamp(models.Model):
    name = models.CharField(max_length=80)
    desc = models.CharField(max_length=1024)

    def __str__(self):
        return "SubCamp: %s" % self.name

    class Admin:
        pass

class CampSite(models.Model):
    subcamp = models.ForeignKey(SubCamp)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=80)
    desc = models.CharField(max_length=1024)
    numpeople = models.IntegerField()

    def __str__(self):
        return "Campsite: %s %d people" % (self.name, self.numpeople)

    class Admin:
        pass

class Area(models.Model):
    campsite = models.ForeignKey(CampSite)
    name = models.CharField(max_length=80)
    desc = models.CharField(max_length=1024)
    width = models.IntegerField()
    height = models.IntegerField()

    def __str__(self):
        return "Area: %s (%d x %d)" % (self.name, self.width, self.height)

    class Admin:
        pass
