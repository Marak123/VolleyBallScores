from typing import Any
from django.db import models
from django.core.exceptions import ValidationError

class RandomOrgRequest(models.Model):
    requestUrl = models.URLField(blank=True, null=True)
    requestBody = models.TextField(blank=True, null=True)
    statusCode = models.IntegerField(blank=True, null=True)
    headers = models.TextField(blank=True, null=True)
    responseBody = models.TextField(blank=True, null=True)
    requestDate = models.DateField(auto_now_add=True, editable=False)
    functionName = models.TextField(blank=True, null=True)

class GroupGame(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, unique=True)

    def __str__(self) -> str:
        return f'Grupa {self.pk}'

class Team(models.Model):
    class Meta:
        ordering = ('name',)

    name = models.CharField(max_length=50, unique=True)
    group = models.ForeignKey(GroupGame, models.PROTECT, related_name="grupa", blank=True, null=True)

    # def __init__(self, *args: Any, **kwargs: Any) -> None:
    #     super().__init__(*args, **kwargs)
    #     self._meta.get_field('group').verbose_name = f"Grupa {self.group.pk}"

    def __str__(self):
        return f'{self.name}'

class Match(models.Model):

    team_one = models.ForeignKey(Team, models.PROTECT, related_name="team_one", verbose_name="Drużyna Pierwsza")
    team_two = models.ForeignKey(Team, models.PROTECT, related_name="team_two", verbose_name="Drużyna Druga")

    team_one_score = models.IntegerField(default=0)
    team_two_score = models.IntegerField(default=0)


    def __str__(self) -> str:
        return f'{self.team_one} vs {self.team_two}'

    def clean(self) -> None:
        if self.team_one == self.team_two:
            raise ValidationError("Nie można stworzyć meczu z dwiema tymi samymi drużynami", 400)

        return super().clean()

    def save(self, *args: Any, **kwargs: Any) -> None:
        self._meta.get_field('team_one_score').verbose_name = f"Punkty '{self.team_one}'"
        self._meta.get_field('team_two_score').verbose_name = f"Punkty '{self.team_two}'"

        super().save(*args, **kwargs)