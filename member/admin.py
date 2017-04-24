from django.contrib import admin
from member.models import BadgeAwards, Badges, BadgeVideos, CoachInstuction, BadgeAssesments, UserMember


class BadgeAwardAdmin(admin.ModelAdmin):
    list_display = ('userId_id', 'badgeId_id', 'dateAwarded')


class UserMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name')


class CoachInstuctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipType', 'description', 'badgeName')


class BadgesAdmin(admin.ModelAdmin):
    list_display2 = ('name', 'category', 'levels')

    class Meta:
        verbose_name_plural = "badges"

admin.site.register(BadgeAwards, BadgeAwardAdmin)
admin.site.register(UserMember, UserMemberAdmin)
admin.site.register(Badges, BadgesAdmin)
admin.site.register(BadgeVideos)
admin.site.register(CoachInstuction, CoachInstuctionAdmin)
admin.site.register(BadgeAssesments)
