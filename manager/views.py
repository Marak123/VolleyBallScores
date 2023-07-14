from django.shortcuts import render, redirect
from django.views.generic.list import ListView, View
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Team, Match, GroupGame
from .forms import RandomAssignTeamToGroup_TeamForms, RandomAssignTeamToGroup_GroupGameForms
from .random_request import DrawNumbers

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
    template_name = 'generic_create.html'
    parent_name = None

    def get_context_data(self, **kwargs):
        context = super(myCreateView, self).get_context_data(**kwargs)
        context['parent_name'] = self.parent_name

        return context

class myUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'generic_update.html'
    parent_name = None

    def get_context_data(self, **kwargs):
        context = super(myUpdateView, self).get_context_data(**kwargs)
        context['parent_name'] = self.parent_name

        return context

class myDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'generic_delete.html'
    parent_name = None

    def get_context_data(self, **kwargs):
        context = super(myDeleteView, self).get_context_data(**kwargs)
        context['parent_name'] = self.parent_name

        return context

class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = 'manager/manager.html'

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
    template_name = 'manager/group_list.html'

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)

        # groups_with_teams = GroupGame.objects.annotate(
        #     assigned_teams=ArrayAgg('team__name', distinct=True)
        # ).values('pk', 'assigned_teams')

        # group_assign = {item['pk']: item['assigned_teams'] for item in groups_with_teams}

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

class RandomAssignTeamToGroup(View):
    template_name = "manager/random_assign.html"

    def get(self, request):
        group_form = RandomAssignTeamToGroup_GroupGameForms()
        team_form = RandomAssignTeamToGroup_TeamForms()
        return render(request, self.template_name, context={'group_form': group_form, 'team_form': team_form})

    def post(self, request):
        group_form = RandomAssignTeamToGroup_GroupGameForms(request.POST)
        team_form = RandomAssignTeamToGroup_TeamForms(request.POST)

        if group_form.is_valid() and team_form.is_valid():
            selected_groups = group_form.cleaned_data['groups']
            selected_teams = team_form.cleaned_data['teams']

# Add checking if team is now assign to some group

            auto_assign_result = self.autoAssign(selected_groups, selected_teams)

            for key, value in auto_assign_result.items():
                group_to_assign = GroupGame.objects.get(pk=key)
                for t in value:
                    team_a = Team.objects.get(pk=t)
                    team_a.group = group_to_assign
                    team_a.save()

            return redirect('manager:group')

        return render(request, self.template_name, {'group_form': group_form, 'team_form': team_form})

    def autoAssign(self, groups: list, teams: list) -> dict:
        draw_num = DrawNumbers()

        groups_len = len(groups)
        teams_len = len(teams)

        if groups_len == 0 or teams_len == 0:
            return {}
        elif groups_len > teams_len:
            groups_len = teams_len
        elif groups_len == 1:
            return { f"{groups[0]}": teams }

        amount_teams_to_group = int(teams_len / groups_len)

        data = { i: amount_teams_to_group for i in range(groups_len) }

        if not (teams_len % groups_len) == 0:
            req = draw_num.getRandomNumber((teams_len % groups_len), 0, groups_len - 1)

            if req['error']['status']:
                print("Error:", req['error']['message'], req['error']['code'])

            for i in req['data']:
                data[i] += 1

        teams_list = teams
        dataRet = {}
        for key,value in data.items():

            teams_list_length = len(teams_list)
            if teams_list_length == value:
                dataRet[f'{groups[key]}'] = teams_list
                break

            get_random_num = draw_num.getRandomNumber(value, 0, teams_list_length - 1)

            if get_random_num['error']['status']:
                print("Error:", get_random_num['error']['message'], req['error']['code'])

            t = []
            for i, v in enumerate(get_random_num['data']):
                t.append(teams_list[i])
                teams_list.pop(i)

            dataRet[f'{groups[key]}'] = t

        return dataRet

# class ManualAssignTeamToGroup(LoginRequiredMixin, View):
#     template_name = "manager/manual_assign.html"

#     def get(self, request):
#         group_form = RandomAssignTeamToGroup_GroupGameForms()
#         team_form = RandomAssignTeamToGroup_TeamForms()
#         return render(request, self.template_name, context={'group_form': group_form, 'team_form': team_form})

#     def post(self, request):
#         group_form = RandomAssignTeamToGroup_GroupGameForms(request.POST)
#         team_form = RandomAssignTeamToGroup_TeamForms(request.POST)

#         if group_form.is_valid() and team_form.is_valid():
#             selected_groups = group_form.cleaned_data['groups']
#             selected_teams = team_form.cleaned_data['teams']

#             print("Group: ", selected_groups)
#             print("Team: ", selected_teams)

#             return redirect('manager:group')

#         return render(request, self.template_name, {'group_form': group_form, 'team_form': team_form})