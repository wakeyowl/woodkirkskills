from django import template
from member.models import BadgeAwards

register = template.Library()


@register.filter(name='getBadgeCount')
def getBadgeCount(list, key):
    if list and isinstance(list, dict) and list.get(key):
        firstlist = list.get(key)
        return firstlist.get('count')

@register.filter(name='getPointsCount')
def getPointsCount(list, key):
    if list and isinstance(list, dict) and list.get(key):
        firstlist = list.get(key)
        return firstlist.get('count')


@register.filter(name='getBadgeData')
def getBadgeData(list, key):
    if list and isinstance(list, dict) and list.get(key):
        firstlist = list.get(key)
        return firstlist.get('player_completion_percent')
