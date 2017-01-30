from django.contrib import admin
from django.utils.html import format_html

import string

from .models import Person, Function, Event, Vote, IPAddress, FrontpageMessage


# From proft.me, wanted to do it fast
class AlphabetFilter(admin.SimpleListFilter):
    title = 'alphabet'
    parameter_name = 'alphabet'

    def lookups(self, request, model_admin):
        abc = list(string.ascii_lowercase)
        return ((c.upper(), c.upper()) for c in abc)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name__startswith=self.value())


class FunctionFilter(admin.SimpleListFilter):
    title = 'function'
    parameter_name = 'function'

    def lookups(self, request, model_admin):
        return ((f.name, f.name) for f in Function.objects.all().order_by('name'))

    def queryset(self, request, queryset):
        if self.value():
            return Function.objects.get(name=self.value()).person_set.all()



class PersonAdmin(admin.ModelAdmin):

    model = Person
    list_display = ('name', 'list_of_functions', 'has_wiki_summary', 'wiki_pagename')
    list_filter = (FunctionFilter, AlphabetFilter,)


class EventAdmin(admin.ModelAdmin):

    model = Event
    # list_display = ('date', 'name', 'who', 'function_at_the_time', 'reported', 'added_recently', 'modified_recently')
    list_display = (
        'date',
        'name',
        'display_who',
        'display_function',
        'online', 'reported',
        'display_submitter',
        'display_submitter_banstate',
    )
    list_filter = ['who']

    def display_who(self, obj):
        return format_html(
            '<a href="/admin/Chronology/person/{pk}/change/">{name}</a>',
            pk=obj.who.id,
            name=obj.who.name
        )
    display_who.short_description = 'Who'

    def display_function(self, obj):
        return format_html(
            '<a href="/admin/Chronology/function/{pk}/change/">{name}</a>',
            pk=obj.function_at_the_time.id,
            name=obj.function_at_the_time.name
        )
    display_function.short_description = 'Function'

    def display_submitter(self, obj):
        if obj.submitter:
            return format_html(
                '<a href="/admin/Chronology/ipaddress/{pk}/change/">{ip}</a>',
                pk=obj.submitter.id,
                ip=obj.submitter.ip
            )
        else:
            return '-'
    display_submitter.short_description = 'Submitter'

    def display_submitter_banstate(self, obj):
        if obj.submitter:
            return obj.submitter.banned
        else:
            return False
    display_submitter_banstate.short_description = 'Sub. banned?'
    display_submitter_banstate.boolean = True



class FunctionAdmin(admin.ModelAdmin):

    model = Function
    list_display = ('name', 'number_of_bearers')
    list_filter = (AlphabetFilter,)


class FrontpageMessageAdmin(admin.ModelAdmin):

    model = FrontpageMessage
    list_display = ('title', 'date')


class IPAddressAdmin(admin.ModelAdmin):

    model = IPAddress
    list_display = ('ip', 'banned', 'banned_since')
    list_filter = ('banned',)


class VoteAdmin(admin.ModelAdmin):

    class Media:
        css = {
                'all': ('css/font-awesome.min.css', 'css/admin_colors.css')
        }

    model = Vote
    list_display = ('__str__', 'voter_ip', 'voter_banned', 'event_name', 'display_vote')
    list_filter = ('vote',)

    def voter_ip(self, obj):
        return format_html(
            '<a href="/admin/Chronology/ipaddress/{pk}/change/">{ip}</a>',
            pk=obj.voter.id,
            ip=obj.voter.ip
        )

    def voter_banned(self, obj):
        return obj.voter.banned
    voter_banned.boolean = True

    def event_name(self, obj):
        return obj.event.name

    def display_vote(self, obj):
        return format_html(
            '<i class="fa {arrow_class}" aria-hidden="true"></i>',
            arrow_class='fa-arrow-up green' if (obj.vote==Vote.UP) else 'fa-arrow-down red'
        )
    display_vote.short_description = 'Vote'


admin.site.register(Event, EventAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Function, FunctionAdmin)
admin.site.register(IPAddress, IPAddressAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(FrontpageMessage, FrontpageMessageAdmin)
