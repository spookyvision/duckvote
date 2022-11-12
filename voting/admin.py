from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from .models import VoteItem, YesNoAbstain, MultipleChoice, VoteEvent, ChoiceOption
from django import forms


admin.site.register((VoteEvent, ChoiceOption))


@admin.register(VoteItem)
class VoteItemParentAdmin(PolymorphicParentModelAdmin):
    """ The parent/abstract vote item model admin """
    child_models = (YesNoAbstain, MultipleChoice)
    # list_filter = (PolymorphicChildModelFilter,)  # This is optional.


class VoteItemBaseForm(forms.ModelForm):
    pass


class VoteItemChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all vote item child models """

    base_form = forms.ModelForm
    base_fieldsets = (
        (None, {
            'fields': ('event', 'description')
        }),
    )


@admin.register(YesNoAbstain)
class YesNoAbstainAdmin(VoteItemChildAdmin):
    show_in_index = True


@admin.register(MultipleChoice)
class MultipleChoiceAdmin(VoteItemChildAdmin):
    show_in_index = True
