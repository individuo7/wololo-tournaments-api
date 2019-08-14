from django.contrib import admin
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


class MatchGameInline(admin.TabularInline):
    extra = 1
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
    extra = 1
    model = CivilizationMatch


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("tournament", "phase", "date", "winner")
    inlines = [PlayerGameInline, MatchGameInline, CivilizationMatchInline]
