from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import path, reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import Team, Match, GroupGame
from .views import TeamListView, RandomAssignTeamToGroup, myCreateView, myDeleteView, myUpdateView, GroupListView
# from .forms import MatchCreateForm


urlpatterns = [
    path('', TeamListView.as_view(), name='manage'),

    # '''
    #     Team Patchs
    # '''

    path('team', login_required(ListView.as_view(
            model=Team,
            template_name='manager/team_list.html'
        )), name='team'),

    path('team/add', myCreateView.as_view(
        model=Team,
        fields=('name',),
        success_url=reverse_lazy('manager:team-create'),
        parent_name="team"
    ), name='team-create'),

    path('team/<int:pk>/remove', myDeleteView.as_view(
        model=Team,
        success_url=reverse_lazy('manager:manage'),
        parent_name="team"
    ), name='team-delete'),

    path('team/<int:pk>/edit', myUpdateView.as_view(
        model=Team,
        fields='__all__',
        success_url=reverse_lazy('manager:manage'),
        parent_name="team"
    ), name='team-edit'),



    # '''
    #     Match Patchs
    # '''

    path('match', login_required(ListView.as_view(
        model=Match,
        template_name='manager/match_list.html'
    )), name='match'),

    path('match/add', myCreateView.as_view(
        model=Match,
        fields=('team_one', 'team_two'),
        success_url=reverse_lazy('manager:match-create'),
        parent_name="match"
    ), name='match-create'),

    path('match/<int:pk>/remove', myDeleteView.as_view(
        model=Match,
        success_url=reverse_lazy('manager:manage'),
        parent_name="match"
    ), name='match-delete'),

    path('match/<int:pk>/edit', myUpdateView.as_view(
        model=Match,
        fields='__all__',
        success_url=reverse_lazy('manager:manage'),
        parent_name="match"
    ), name='match-edit'),

    # '''
    #     Add Points Patchs
    # '''

    # path('match/<int:pk>/add-point', login_required(UpdateView.as_view(
    #     model=Match,
    #     fields=('team_one_score', 'team_two_score'),
    #     success_url=reverse_lazy('manager:manage'),
    #     template_name='generic_update.html'
    # )), name='match-add-point'),

    # '''
    #     Group Patchs
    # '''

    path('group', GroupListView.as_view(), name='group'),

    path('group/add', myCreateView.as_view(
        model=GroupGame,
        fields='__all__',
        success_url=reverse_lazy('manager:group-create'),
        parent_name="group"
    ), name='group-create'),

    path('group/<int:pk>/remove', myDeleteView.as_view(
        model=GroupGame,
        success_url=reverse_lazy('manager:manage'),
        parent_name="group"
    ), name='group-delete'),

    path('group/<int:pk>/edit', myUpdateView.as_view(
        model=GroupGame,
        fields='__all__',
        success_url=reverse_lazy('manager:manage'),
        parent_name="group"
    ), name='group-edit'),

    path('group/random-assign', login_required(RandomAssignTeamToGroup.as_view()), name="random-assign-group"),
    # path('group/manual-assign', login_required(ManualAssignTeamToGroup.as_view()), name="manual-assign-group"),


    # # assign team to group
    # path('assign-to-group', login_required(UpdateView.as_view(
    #     model=Match,
    #     fields=('team_one_score', 'team_two_score'),
    #     success_url=reverse_lazy('manager:manage'),
    #     template_name='generic_update.html'
    # )), name='assign-to-group'),

    # # auto assign team to group
    # path('auto-assign-to-group', login_required(UpdateView.as_view(
    #     model=Match,
    #     fields=('team_one_score', 'team_two_score'),
    #     success_url=reverse_lazy('manager:manage'),
    #     template_name='generic_update.html'
    # )), name='auto-assign-to-group'),
]
