from django.contrib import admin

from member.models import BadgeAwards, Badges, BadgeMedia, CoachInstuction, BadgeAssesments, UserMember, TeamManagers, \
    User, PlayerMatchAwards

admin.site.unregister(User)


def change_password(modeladmin, request, queryset):
    queryset.update(password="pbkdf2_sha256$30000$tmJztDx7lgtg$CrOItg+7R2H2y+9VjZX9yY5xbP9zw8oGAxxC7Pn704w=")


change_password.short_description = "Set Temporary Password"


@admin.register(BadgeAwards)
class BadgeAwardAdmin(admin.ModelAdmin):
    list_display = ('userId_id', 'badgeId_id', 'dateAwarded', 'score', 'comments', 'managerId_id')
    list_filter = ('badgeId_id', 'managerId_id',)


pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_joined')
    list_filter = ('date_joined',)
    search_fields = ('first_name', 'email', 'username')
    actions = [change_password, ]
    ordering = ('username',)

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
    list_display = ('description', 'name', 'category', 'levels',)
    list_filter = ('levels', 'category', 'name',)


pass


@admin.register(TeamManagers)
class TeamManagerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'team')
    list_filter = ('full_name', 'team')


pass


@admin.register(BadgeMedia)
class BadgeMediaAdmin(admin.ModelAdmin):
    list_display = ('badgeId', 'pageUrl', 'description', 'mediaType')
    ordering = ('badgeId',)


pass


@admin.register(PlayerMatchAwards)
class PlayerMatchAwardsAdmin(admin.ModelAdmin):
    list_display = ('userId', 'dateAwarded', 'awardType', 'score', 'comments')

pass
