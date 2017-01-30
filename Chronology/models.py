from django.db import models
from django.utils import timezone

from datetime import timedelta

from .signal_handlers import wikipedia_fill_handler
from .utils import fill_with_wikipedia


class Function(models.Model):
    """
    Stores function information
    such as 'President of the United State'
    """

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def number_of_bearers(self):
        return self.person_set.count()


class Person(models.Model):
    """
    Store Person details
    A given person may have several function at the same time
    """

    name = models.CharField(max_length=100)
    wiki_summary = models.TextField(blank=True, default='')
    wiki_pagename = models.CharField(max_length=200, blank=True, default='')
    functions = models.ManyToManyField(Function, blank=True)

    def __str__(self):
        return self.name

    def force_wikipedia_fill(self):
        fill_with_wikipedia(self)
        self.save()

    def has_wiki_summary(self):
        return self.wiki_summary!=''
    has_wiki_summary.boolean = True
    has_wiki_summary.short_description = 'Has Summary ?'

    def list_of_functions(self):
        repr = ', '.join(map(str, self.functions.all()))
        if len(repr)>51:
            repr = repr[:50]+"…"
        return  repr if len(repr) else 'None'
    list_of_functions.short_description = 'Functions'


class IPAddress(models.Model):
    """ Store IPs and bans"""

    ip = models.CharField(max_length=15, unique=True)
    banned = models.BooleanField(default=False)
    banned_since = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "%s (banned since %s)"%(self.ip, self.banned_since) if self.banned else '%s'%(self.ip,)

    @classmethod
    def is_banned(cls, ip_address):
        return cls.objects.filter(ip=ip_address, banned=True).count()>0


class Event(models.Model):
    """ Stores Events """

    date = models.DateField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    who = models.ForeignKey(Person)
    description = models.TextField(blank=True)
    function_at_the_time = models.ForeignKey(Function)
    reported = models.BooleanField(default=False)
    online = models.BooleanField(default=True)
    submitter = models.ForeignKey(IPAddress, blank=True, null=True)

    def __str__(self):
        return "%s by %s on the %s"%(self.name, self.who, self.date)

    def save(self, *args, **kwargs):

        if self.function_at_the_time not in self.who.functions.all():
            self.who.functions.add(self.function_at_the_time)
            self.who.save()

        super().save(*args, **kwargs)

    def added_recently(self):

        nowM12 = timezone.now()-timedelta(hours=12)
        return (self.date_added>nowM12)
    added_recently.boolean = True
    added_recently.short_description = 'Added Recently'

    def modified_recently(self):

        nowM12 = timezone.now()-timedelta(hours=12)
        return (self.date_modified>nowM12)
    modified_recently.boolean = True
    modified_recently.short_description = 'Modified Recently'


class Vote(models.Model):
    """ Stores votes """
    UP = 'up'
    DOWN = 'down'
    NEUTRAL = 'neutral'
    VOTE_CHOICES = (
        (UP, 'Up'),
        (DOWN, 'Down'),
        (NEUTRAL, 'Neutral')
    )

    vote = models.CharField(choices=VOTE_CHOICES, max_length=7)
    voter = models.ForeignKey(IPAddress)
    event = models.ForeignKey(Event)


class FrontpageMessage(models.Model):
    """ Allows display of messages on the frontpage """

    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return "%s (on %s)"%(self.title, self.date)


models.signals.pre_save.connect(wikipedia_fill_handler, sender=Person)
