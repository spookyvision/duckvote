from .models import YesNoAbstain
from django import forms
from typing import Any
from django.shortcuts import render, redirect
from .models import VoteEvent, VoteItem, YNAVote
from django.views.generic.edit import CreateView, UpdateView, FormMixin
from django.urls import reverse_lazy, reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseServerError


def do_login(request, user_id=None):
    logout(request)
    user = authenticate(request, user_id=user_id)
    if user is not None:
        login(request, user)
        return redirect('voting:index')
    else:
        return HttpResponseServerError()


@staff_member_required
def stats(request):
    pass


@login_required
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
            url = reverse('voting:update_yna',  kwargs={
                          'yna_id': item.id, 'pk': vote.id})
        vote_data = {'vote': vote, 'url': url}
        items_votes.append((item, vote_data))
    context = {'event': event, 'items_votes': items_votes,
               'username': request.user.username}
    # User.objects.filter(pk=1).prefetch_related('ynavote_set', 'choicevote_set')
    return render(request, 'voting/index.html', context)


class YNAForm(forms.ModelForm):
    class Meta:
        model = YNAVote
        fields = ['choice']
        widgets = {
            'choice': forms.RadioSelect()
        }

    def clean(self):
        event: VoteEvent = YesNoAbstain.objects.get(pk=self.yna_id).event
        if not event.has_started():
            raise ValidationError(_('Voting has not started yet!'))
        if event.has_ended():
            raise ValidationError(_('Voting has ended!'))
        cleaned_data = super().clean()
        return cleaned_data


class YNAMixin:
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        res = super().get_context_data(**kwargs)
        item = YesNoAbstain.objects.get(pk=self.kwargs['yna_id'])
        res['title'] = item.description
        return res

    def get_form(self, form_class=None):
        res = super().get_form(form_class)
        res.yna_id = self.kwargs['yna_id']
        return res


class YNACreateView(LoginRequiredMixin, YNAMixin, CreateView):
    model = YNAVote
    form_class = YNAForm
    success_url = reverse_lazy('voting:index')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        form.instance.yna_id = self.kwargs['yna_id']
        return super().form_valid(form)


class YNAUpdateView(LoginRequiredMixin, YNAMixin, UpdateView):
    model = YNAVote
    form_class = YNAForm
    success_url = reverse_lazy('voting:index')
