from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist

from .models import Person, IPAddress, Vote, Event, Function, FrontpageMessage
from .utils import get_client_ip
from .forms import EventForm


def index(request, form=None):
    """
    Index view -- homepage

    Must serve the timeline & the eventual message
    """

    # get the messages
    msg_count =  FrontpageMessage.objects.count()
    if msg_count:
        message = FrontpageMessage.objects.all().order_by('-date')[0]
    else:
        message = None

    # get the event
    events = Event.objects.all().order_by('-date')

    # get the form and the different autocomplete options
    if not form:
        form = EventForm()
    who_options = Person.objects.values_list('name', flat=True).order_by('name')
    function_options = Function.objects.values_list('name', flat=True).order_by('name')

    return render(
        request,
        'index.html',
        {
            'events': events,
            'message': message,
            'form': form,
            'who_options': who_options,
            'function_options': function_options
        }
    )


class EventDetail(generic.DetailView):
    model = Event
    template_name = 'event_detail.html'


def event_vote(request, pk, vote_order):
    """
    Checks if the Event exist, if the user hasn't already voted
    in the same direction and forge a Vote object accordingly or
    modify the retrieved Vote
    """

    # check if Event exists and get it if so
    e = get_object_or_404(Event, pk=pk)

    ip_raw = get_client_ip(request)
    ip, ip_created = IPAddress.objects.get_or_create(ip=ip_raw)
    # before altering the DB, check if the IP is banned
    if ip.banned:
        return render(request, 'forbidden.html', {'ip': ip}, status=403)

    # if the IP was already in DB, maybe it already voted
    if not ip_created:
        try:
            vote = Vote.objects.get(event=e, voter=ip)
        except ObjectDoesNotExist:
            vote = None
    vote = None

    # do nothing if re-voting
    if vote and (vote.vote==vote_order):
        return redirect('index')

    # change event's score
    e.score += 1 if vote_order==Vote.UP else -1
    e.save()

    if not vote:
        vote = Vote.objects.create(voter=ip, vote=vote_order, event=e)
    else:
        vote_states_dict = { Vote.DOWN:0, Vote.NEUTRAL:1, Vote.UP:2 }
        vote_states = [Vote.DOWN, Vote.NEUTRAL, Vote.UP]

        increment = +1 if vote_order==Vote.UP else -1
        vote.vote = vote_states[vote_states_dict[vote.vote]+increment]
        vote.save()

    return redirect('index')



def event_report(request, pk):
    pass


def event_add(request):
    """ Add an event, creating Person and Function object on-the-fly if needed"""
    if request.method=='POST':

        ip_raw = get_client_ip(request)
        ip, ip_created = IPAddress.objects.get_or_create(ip=ip_raw)
        # before altering the DB, check if the IP is banned
        if ip.banned:
            return render(request, 'forbidden.html', {'ip': ip}, status=403)

        form = EventForm(request.POST)
        if not form.is_valid():
            return index(request, form)

        function, func_created = Function.objects.get_or_create(name=form.cleaned_data['function'])
        person, pers_created = Person.objects.get_or_create(name=form.cleaned_data['who'])

        # assign the function if needed
        if not function in person.functions.all():
            person.functions.add(function)
            person.save()

        e = Event.objects.create(
            date = form.cleaned_data['date'],
            name = form.cleaned_data['name'],
            who = person,
            description = form.cleaned_data['description'],
            function_at_the_time = function,
            submitter = ip
        )

    return redirect('index')

