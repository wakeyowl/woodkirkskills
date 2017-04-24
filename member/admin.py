from django.contrib import admin
from member.models import BadgeAwards, Badges, BadgeVideos, CoachInstuction, BadgeAssesments


class BadgeAwardAdmin(admin.ModelAdmin):
    list_display = ('userId_id', 'badgeId_id', 'dateAwarded')


class CoachInstuctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipType', 'description', 'badgeName')


class BadgesAdmin(admin.ModelAdmin):
    list_display2 = ('name', 'category', 'levels')

    class Meta:
        verbose_name_plural = "badges"

admin.site.register(BadgeAwards, BadgeAwardAdmin)
admin.site.register(Badges, BadgesAdmin)
admin.site.register(BadgeVideos)
admin.site.register(CoachInstuction, CoachInstuctionAdmin)
admin.site.register(BadgeAssesments)
