from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import path, reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import Team, Match, GroupGame
from .views import TeamListView, RandomAssignTeamToGroup, myCreateView, myDeleteView, myUpdateView, GroupListView, addPointToMatch, AutoCreateMatchView, ClearAssignGroupView, RemoveAllMatchView, AutoPlayOrderingView, ManageMatchView, finishData
# from .forms import MatchCreateForm


urlpatterns = [
    path('', TeamListView.as_view(), name='manage'),

    # '''
    #     Team Patchs
    # '''

    path('team', login_required(ListView.as_view(
            model=Team,
            template_name='manager/team_list.dhtml'
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
        template_name='manager/match_list.dhtml'
    )), name='match'),

    path('match/<int:pk>', ManageMatchView.as_view(), name="match-manage"),

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

    path('match/remove-all-match', RemoveAllMatchView, name="remove-all-match"),
    path('match/auto-create', AutoCreateMatchView.as_view(), name="auto-create-match"),
    path('match/play-order', AutoPlayOrderingView.as_view(), name="auto-play-ordering-match"),
    path('match/<int:pk>/add-point', addPointToMatch, name='match-add-point'),
    path('match/<int:pk>/finish-data', finishData, name='match-add-point'),

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

    path('group/clear-assign', ClearAssignGroupView, name="clear-assign-group"),
    path('group/random-assign', RandomAssignTeamToGroup.as_view(), name="random-assign-group"),
    # path('group/manual-assign', login_required(ManualAssignTeamToGroup.as_view()), name="manual-assign-group"),

]
