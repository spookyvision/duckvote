from django.shortcuts import render
from .models import VoteEvent, VoteItem


def index(request):
    events = VoteEvent.objects.order_by('-start_at')
    event = events.first()
    items = VoteItem.objects.filter(event=event)
    context = {'event': event, 'items': items}
    # User.objects.filter(pk=1).prefetch_related('ynavote_set', 'choicevote_set')
    return render(request, 'voting/index.html', context)


def vote_multiple_choice(request):
    context = {}
    return render(request, 'voting/vote_multiple_choice.html', context)


def vote_yna(request):
    context = {}
    return render(request, 'voting/vote_yna.html', context)
