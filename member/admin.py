from django.contrib import admin
from member.models import BadgeAwards, Badges, BadgeVideos, CoachInstuction, BadgeAssesments, UserMember


class BadgeAwardAdmin(admin.ModelAdmin):
    list_display = ('userId_id', 'badgeId_id', 'dateAwarded')


class UserMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name')


class BadgeAssessmentsAdmin(admin.ModelAdmin):
    list_display = ('badgeId', 'description')


class CoachInstuctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipType', 'description', 'badgeName')


class BadgesAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'levels')


class BadgeVideosAdmin(admin.ModelAdmin):
    list_display = ('badgeId', 'pageUrl', 'description', )


admin.site.register(BadgeAwards, BadgeAwardAdmin)
admin.site.register(UserMember, UserMemberAdmin)
admin.site.register(Badges, BadgesAdmin)
admin.site.register(BadgeVideos, BadgeVideosAdmin)
admin.site.register(CoachInstuction, CoachInstuctionAdmin)
admin.site.register(BadgeAssesments, BadgeAssessmentsAdmin)
