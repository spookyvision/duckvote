from .models import YesNoAbstain
from django import forms
from typing import Any
from django.shortcuts import render
from .models import VoteEvent, VoteItem, YNAVote
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy, reverse


def index(request):
    events = VoteEvent.objects.order_by('-start_at')
    event = events.first()
    items = VoteItem.objects.filter(event=event)
    items_votes = []
    for item in items:
        vote = item.user_vote(request.user)
        if vote is None:
            url = reverse('voting:create_yna',  kwargs={'yna_id': item.id})
        else:
            url = reverse('voting:update_yna',  kwargs={'pk': vote.id})
        vote_data = {'vote': vote, 'url': url}
        items_votes.append((item, vote_data))
    context = {'event': event, 'items_votes': items_votes}
    # User.objects.filter(pk=1).prefetch_related('ynavote_set', 'choicevote_set')
    return render(request, 'voting/index.html', context)


def vote_multiple_choice(request):
    context = {}
    return render(request, 'voting/vote_multiple_choice.html', context)


def vote_yna(request):
    context = {}
    return render(request, 'voting/vote_yna.html', context)


class YNAForm(forms.ModelForm):
    class Meta:
        model = YNAVote
        fields = ['choice']
        widgets = {
            'choice': forms.RadioSelect()
        }


class YNACreateView(CreateView):
    model = YNAVote
    form_class = YNAForm
    success_url = reverse_lazy('voting:index')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        res = super().get_context_data(**kwargs)
        item = YesNoAbstain.objects.get(pk=self.kwargs['yna_id'])
        res['title'] = item.description
        return res

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        form.instance.yna_id = self.kwargs['yna_id']
        return super().form_valid(form)


class YNAUpdateView(UpdateView):
    model = YNAVote
    form_class = YNAForm
    success_url = reverse_lazy('voting:index')
