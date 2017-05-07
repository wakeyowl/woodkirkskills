from django.contrib import admin
from member.models import BadgeAwards, Badges, BadgeMedia, CoachInstuction, BadgeAssesments, UserMember, TeamManagers


class BadgeAwardAdmin(admin.ModelAdmin):
    list_display = ('userId_id', 'badgeId_id', 'dateAwarded')


class UserMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'favourite_player', 'favourite_team', 'managerId_id')


class BadgeAssessmentsAdmin(admin.ModelAdmin):
    list_display = ('badgeId', 'description')


class CoachInstuctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipType', 'description', 'badgeName')


class BadgesAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'levels')


class TeamManagerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'team')


class BadgeMediaAdmin(admin.ModelAdmin):
    list_display = ('badgeId', 'pageUrl', 'description', 'mediaType')


admin.site.register(BadgeAwards, BadgeAwardAdmin)
admin.site.register(UserMember, UserMemberAdmin)
admin.site.register(Badges, BadgesAdmin)
admin.site.register(BadgeMedia, BadgeMediaAdmin)
admin.site.register(CoachInstuction, CoachInstuctionAdmin)
admin.site.register(BadgeAssesments, BadgeAssessmentsAdmin)
admin.site.register(TeamManagers, TeamManagerAdmin)
