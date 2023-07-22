from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.views.generic.list import ListView, View
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from .models import Team, Match, GroupGame, MatchesOrder
from .forms import RandomAssignTeamToGroupForms, AutoCreateMatchForms, AutoPlayOrderingForms
from .random_request import RandomAssign

import json

# class TeamListView(ListView):
#     model = Team
#     paginate_by = 5

#     def get_context_data(self, *, object_list=None, **kwargs):
#         queryset = object_list if object_list is not None else self.object_list

#         form = ExpenseSearchForm(self.request.GET)
#         if form.is_valid():
#             name = form.cleaned_data.get('name', '').strip()

#         return super().get_context_data(
#             form=form,
#             object_list=queryset,
#             summary_per_category=summary_per_category(queryset),
#             total_amount_spent=total_amount_spent(queryset),
#             total_summary_per_year_month=total_summary_per_year_month(queryset),
#             total_summary_per_year=total_summary_per_year(queryset),
#             **kwargs)

class myCreateView(LoginRequiredMixin, CreateView):
    template_name = 'generic_create.dhtml'
    parent_name = None

    def get_context_data(self, **kwargs):
        context = super(myCreateView, self).get_context_data(**kwargs)
        context['parent_name'] = self.parent_name

        return context

class myUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'generic_update.dhtml'
    parent_name = None

    def get_context_data(self, **kwargs):
        context = super(myUpdateView, self).get_context_data(**kwargs)
        context['parent_name'] = self.parent_name

        return context

class myDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'generic_delete.dhtml'
    parent_name = None

    def get_context_data(self, **kwargs):
        context = super(myDeleteView, self).get_context_data(**kwargs)
        context['parent_name'] = self.parent_name

        return context

class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = 'manager/manager.dhtml'

    def get_context_data(self, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)
        context.update({
            'matchs': Match.objects.all(),
            'teams': Team.objects.all(),
            'groups': GroupGame.objects.all(),
        })

        return context

class GroupListView(LoginRequiredMixin, ListView):
    model = GroupGame
    template_name = 'manager/group_list.dhtml'

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)

        result_dict = {}
        groups_with_teams = GroupGame.objects.values('pk', 'name')
        for group in groups_with_teams:
            team_names = Team.objects.filter(group_id=group['pk']).values_list('name', 'pk')
            result_dict[(group['name'], group['pk'])] = list(team_names)

        context.update({
            'matchs': Match.objects.all(),
            'teams': Team.objects.all(),
            'groups': GroupGame.objects.all(),
            'group_assign': result_dict,
        })

        return context


class RandomAssignTeamToGroup(LoginRequiredMixin, View):
    template_name = "manager/random_assign.dhtml"

    def get(self, request):
        form = RandomAssignTeamToGroupForms()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = RandomAssignTeamToGroupForms(request.POST)

        if form.is_valid():
            selected_groups = form.cleaned_data['groups']
            selected_teams = form.cleaned_data['teams']

# Add checking if team is now assign to some group
            ra = RandomAssign()
            auto_assign_result = ra.autoAssign(selected_groups, selected_teams)

            for key, value in auto_assign_result.items():
                group_to_assign = GroupGame.objects.get(pk=key)
                for t in value:
                    team_a = Team.objects.get(pk=t)
                    team_a.group = group_to_assign
                    team_a.save()

            return redirect('manager:group')

        return render(request, self.template_name, {'form': form,})

class AutoCreateMatchView(LoginRequiredMixin, View):
    template_name = "manager/auto_create_match.dhtml"

    def get(self, request):
        form = AutoCreateMatchForms()

        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = AutoCreateMatchForms(request.POST)

        if form.is_valid():
            by_what = form.cleaned_data['by_team_or_group']
            selected_groups = form.cleaned_data['groups']
            selected_teams = form.cleaned_data['teams']

            if int(by_what) == 0:
                for iO, team in enumerate(selected_teams):
                    for team_sec in selected_teams[iO+1:]:
                        Match.objects.create(
                            team_one=Team.objects.get(pk=int(team)),
                            team_two=Team.objects.get(pk=int(team_sec))
                        ).save()

            elif int(by_what) == 1:
                for group in selected_groups:
                    allTeams = Team.objects.filter(group__pk=group).all()
                    for iO, team in enumerate(allTeams):
                        for team_sec in allTeams[iO+1:]:
                            Match.objects.create(
                                team_one=team,
                                team_two=team_sec
                            ).save()

            return redirect("manager:match")

        return render(request, self.template_name, context={'form': form})

class AutoPlayOrderingView(LoginRequiredMixin, View):
    template_name = "manager/auto_play_ordering.dhtml"

    def get(self, request):
        form = AutoPlayOrderingForms()

        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = AutoPlayOrderingForms(request.POST)

        if form.is_valid():
            pass

            return redirect("manager:match")

        return render(request, self.template_name, context={'form': form})

class ManageMatchView(LoginRequiredMixin, View):
    template_name = "manager/match_manage.dhtml"

    def get(self, request, pk):
        match = Match.objects.get(pk=pk)

        return render(request, self.template_name, context={'match': match})

    def post(self, request):
        form = AutoPlayOrderingForms(request.POST)

        if form.is_valid():
            pass

            return redirect("manager:match")

        return render(request, self.template_name, context={'form': form})




@login_required
def ClearAssignGroupView(request):
    Team.objects.all().update(group=None)
    return redirect('manager:group')

@login_required
def RemoveAllMatchView(request):
    Match.objects.all().delete()
    return redirect("manager:match")


@csrf_protect
@require_POST
def addPointToMatch(request, pk):
    request_data = json.loads(request.body)

    if not ('team_id' in request_data or 'point' in request_data or 'match_id' in request_data):
        data = {
            "error": 400,
            "message": "Invalid data",
            "data": request.POST
        }
        return JsonResponse(data, safe=False)

    try:
        match = Match.objects.filter(pk=pk).first()
        team = Team.objects.filter(pk=request_data['team_id']).first()
    except Match.DoesNotExist or Team.DoesNotExist:
        return JsonResponse({
            "error": 400,
            "message": "Invalid data"
        }, safe=False)


    if match.team_one == team:
        Match.objects.filter(pk=pk).update(team_one_score=int(request_data['point']))
    elif match.team_two == team:
        Match.objects.filter(pk=pk).update(team_two_score=int(request_data['point']))
    else:
        data = {
            "error": 400,
            "message": "Invalid data"
        }
        return JsonResponse(data, safe=False)

    return JsonResponse({
        "match_id": match.pk,
        "team_one_id": match.team_one.pk,
        "team_two_id": match.team_two.pk,
        "team_one_score": match.team_one_score,
        "team_two_score": match.team_two_score,
    })

@csrf_protect
@require_POST
def finishData(request, pk):
    request_data = json.loads(request.body)

    if not ('finished' in request_data or 'team_one_score' in request_data or 'team_two_score' in request_data or 'match_id' in request_data):
        data = {
            "error": 400,
            "message": "Invalid data",
            "data": request.POST
        }
        return JsonResponse(data, safe=False)

    try:
        match = Match.objects.filter(pk=pk).first()
        Match.objects.filter(pk=pk).update(team_one_score=int(request_data['team_one_score']))
        Match.objects.filter(pk=pk).update(team_two_score=int(request_data['team_two_score']))
        Match.objects.filter(pk=pk).update(finished=int(request_data['finished']))
    except Match.DoesNotExist or Team.DoesNotExist:
        return JsonResponse({
            "error": 400,
            "message": "Invalid data"
        }, safe=False)

    return JsonResponse({
        "match_id": match.pk,
        "team_one_id": match.team_one.pk,
        "team_two_id": match.team_two.pk,
        "team_one_score": match.team_one_score,
        "team_two_score": match.team_two_score,
        "finish": match.finished
    })