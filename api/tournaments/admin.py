from django.contrib import admin
from django.forms.models import ModelForm
from .models import CivilizationMatch, Game, Player, PlayerGame, Team, Tournament, Match


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ("name", "prize", "web")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "competitive")


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "country")


class PlayerGameInline(admin.TabularInline):
    extra = 2
    model = PlayerGame


class AlwaysChangedModelForm(ModelForm):
    def has_changed(self):
        """ Should returns True if data differs from initial.
        By always returning true even unchanged inlines will get validated and saved."""
        return True


class MatchGameInline(admin.TabularInline):
    extra = 0
    form = AlwaysChangedModelForm
    model = Match

    readonly_fields = ("civilizations",)

    def civilizations(self, obj):
        player_civ = " and ".join(
            [
                "{}:{}".format(x.player.name, x.civilization)
                for x in obj.civilizations.all()
            ]
        )
        return "civs: {}".format(player_civ)


class CivilizationMatchInline(admin.TabularInline):
    extra = 2
    model = CivilizationMatch


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    search_fields = ["tournament__name", "slug"]
    list_display = ("tournament", "phase", "player_list", "date", "slug", "winner")
    inlines = [PlayerGameInline, MatchGameInline, CivilizationMatchInline]
