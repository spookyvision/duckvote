from django.forms import ModelForm
from .models import YNAVote


class YNAForm(ModelForm):
    class Meta:
        model = YNAVote
        fields = ['choice']
