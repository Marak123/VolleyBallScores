from django import forms
from .models import Match, Team, GroupGame
from django.core.exceptions import ValidationError


# class MatchCreateForm(forms.ModelForm):
#     class Meta:
#         model = Match
#         fields = ('team_one', 'team_two')

#     def clean(self):
#         if self.cleaned_data.get('team_one') == self.cleaned_data.get('team_two'):
#             raise ValidationError("Nie można stworzyć meczu z dwiema tymi samymi drużynami", 400)

class RandomAssignTeamToGroup_TeamForms(forms.ModelForm):
    teams = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Team
        fields = ('teams',)

    def __init__(self, *args, **kwargs):
        super(RandomAssignTeamToGroup_TeamForms, self).__init__(*args, **kwargs)
        self.fields['teams'].choices = [(team.pk, team.name) for team in Team.objects.all()]


class RandomAssignTeamToGroup_GroupGameForms(forms.ModelForm):
    groups = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = GroupGame
        fields = ('groups',)

    def __init__(self, *args, **kwargs):
        super(RandomAssignTeamToGroup_GroupGameForms, self).__init__(*args, **kwargs)
        self.fields['groups'].choices = [(group.pk, group.name) for group in GroupGame.objects.all()]