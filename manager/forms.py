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

class RandomAssignTeamToGroupForms(forms.Form):
    teams = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())
    groups = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())

    class Meta:
        fields = ('teams', 'groups')

    def __init__(self, *args, **kwargs):
        super(RandomAssignTeamToGroupForms, self).__init__(*args, **kwargs)
        self.fields['teams'].choices = [(team.pk, team.name) for team in Team.objects.all()]
        self.fields['groups'].choices = [(group.pk, group.name) for group in GroupGame.objects.all()]

class AutoCreateMatchForms(forms.Form):
    by_team_or_group = forms.ChoiceField(choices=((0, "Według Drużyn"), (1, "Według Grup")), label="Według Czego Tworzyć")
    teams = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), label="Drużyny", required=False)
    groups = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), label="Grupy", required=False)

    class Meta:
        fields = ("by_team_or_group", "teams", "groups")

    def __init__(self, *args, **kwargs):
        super(AutoCreateMatchForms, self).__init__(*args, **kwargs)
        self.fields['teams'].choices = [(team.pk, team.name) for team in Team.objects.all()]
        self.fields['groups'].choices = [(group.pk, group.name) for group in GroupGame.objects.all()]

class MatchAddPointForms(forms.Form):
    match_id = forms.IntegerField()
    team_id = forms.IntegerField()
    point = forms.IntegerField()

    def clean(self):
        form_data = self.cleaned_data

        match_by_pk = Match.objects.filter(pk=form_data['match_id'])
        if not match_by_pk.__len__() == 1:
            raise ValidationError(
                        _("Invalid match id: %(value)s"),
                        code="invalid",
                        params={"value": form_data['match_id']},
                    )

        team_by_pk = Team.objects.filter(pk=form_data['team_id'])
        if not team_by_pk.__len__() == 1:
            raise ValidationError(
                        _("Invalid team id: %(value)s"),
                        code="invalid",
                        params={"value": form_data['team_id']},
                    )

        if not match_by_pk.team_one == team_by_pk or not match_by_pk.team_two == team_by_pk:
            raise ValidationError(
                        _("Team with id %(team_id)s is not in the match with id %(match_id)s"),
                        code="invalid",
                        params={"team_id": form_data['team_id'], "match_id": form_data['match_id']},
                    )

        if form_data['point_add'] == 0:
            raise ValidationError(
                        _("The value of points to be added must be at least one"),
                        code="invalid",
                    )

        return form_data

    def save(self, commit=True, *args, **kwargs):
        m = super(MatchAddPointForms, self).save(commit=False, *args, **kwargs)

        match_by_id = Match.objects.get(pk=self.cleaned_data['match_id'])
        team_by_id = Team.objects.get(pk=self.cleaned_data['team_id'])

        if match_by_id.team_one == team_by_id:
            match_by_id.team_one_score += int(self.cleaned_data['point_add'])
        elif match_by_id.team_two == team_by_id:
            match_by_id.team_two_score += int(self.cleaned_data['point_add'])

        match_by_id.save()

        return m

class AutoPlayOrderingForms(forms.Form):
    ordering = forms.ChoiceField(choices=((0, "Losowo"), (1, "Jak najkrótrzy czas czekania")), label="Sposób układania kolejności")
    match = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), label="Mecze", required=True)

    def __init__(self, *args, **kwargs):
        super(AutoPlayOrderingForms, self).__init__(*args, **kwargs)
        self.fields['match'].choices = [(match.pk, match) for match in Match.objects.all()]
