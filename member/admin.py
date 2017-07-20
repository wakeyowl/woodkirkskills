from django.contrib import admin
from member.models import BadgeAwards, Badges, BadgeMedia, CoachInstuction, BadgeAssesments, UserMember, TeamManagers


@admin.register(BadgeAwards)
class BadgeAwardAdmin(admin.ModelAdmin):
    list_display = ('userId_id', 'badgeId_id', 'dateAwarded', 'score', 'comments', 'managerId_id')
    list_filter = ('badgeId_id', 'managerId_id', )
pass


@admin.register(UserMember)
class UserMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'favourite_player', 'favourite_team', 'managerId_id')
pass


@admin.register(BadgeAssesments)
class BadgeAssessmentsAdmin(admin.ModelAdmin):
    list_display = ('badgeId', 'description')
pass


@admin.register(CoachInstuction)
class CoachInstuctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipType', 'description', 'badgeName')
pass


@admin.register(Badges)
class BadgesAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'levels')
pass


@admin.register(TeamManagers)
class TeamManagerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'team')
    list_filter = ('full_name', 'team')
pass


@admin.register(BadgeMedia)
class BadgeMediaAdmin(admin.ModelAdmin):
    list_display = ('badgeId', 'pageUrl', 'description', 'mediaType')
pass
