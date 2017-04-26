from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import ListView
from registration.backends.simple.views import RegistrationView
from os.path import normpath, basename
from member.forms import UserMemberForm
from member.models import UserMember, Contact, Badges, BadgeAssesments, BadgeVideos, CoachInstuction


class WoodkirkRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('register_profile')


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")
    # last_visit_time = datetime.now()
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).seconds > 0:
        visits += 1
        # update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        # set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    # update/set the visits cookie
    request.session['visits'] = visits


@login_required
def register_profile(request):
    form = UserMemberForm()
    if request.method == 'POST':
        form = UserMemberForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect('index')
        else:
            print(form.errors)

    context_dict = {'form': form}

    return render(request, 'member/profile_registration.html', context_dict)


def index(request):
    response = render(request, 'member/skillsmatrix.html', {})
    return response


def challengebadges(request):
    meritbadge_list = Badges.objects.filter(levels='M')
    badge_counts = {}
    for badge_cat in meritbadge_list:
        if not badge_counts.has_key(badge_cat.levels):
            badge_counts[badge_cat.levels] = {
                'item': badge_cat.levels,
                'count': 0
            }

        badge_counts[badge_cat.levels]['count'] += 1

    badgeassessment_list = BadgeAssesments.objects.all()
    badge_videos = BadgeVideos.objects.all()
    context_dict = {'badgecounts': badge_counts, 'merit': meritbadge_list, 'meritassessments': badgeassessment_list, 'badgevideos': badge_videos}
    response = render(request, 'member/skillchallengebadges.html', context=context_dict)
    return response


def mybadges(request):
    context_dict = get_badge_dictionaries_levels(request, True)
    response = render(request, 'member/mybadges.html', context=context_dict)
    return response


def allbadges(request):
    context_dict = get_badge_dictionaries_levels(request, False)
    response = render(request, 'member/allbadges.html', context=context_dict)
    return response


def get_badge_dictionaries_by_name(request, current_user_only):
    # get the current user and filter the query
    # inner join the badges -> badgeawards
    # filter only the current users badges

    if current_user_only:
        current_user = request.user.pk
        q = Badges.objects.exclude(badgeawards__userId__badgeawards__isnull=True)
        q3 = q.filter(badgeawards__userId=current_user)

    else:
        q3 = Badges.objects.all()

    # q3 = q.filter(badgeawards__userId=current_user)
    # Create a dict of category levels and counts used in custom_tags
    badge_counts = {}
    for badge_cat in q3:
        if not badge_counts.has_key(badge_cat.levels):
            badge_counts[badge_cat.levels] = {
                'item': badge_cat.levels,
                'count': 0
            }

        badge_counts[badge_cat.levels]['count'] += 1

    request_url = request
    # Get Lists of all urls for each section
    badge_by_name_urls = q3.filter(pageUrl__contains=request_url.path)

    # throw back the dictionary

    return badge_by_name_urls


def get_badge_dictionaries_levels(request, current_user_only):
    # get the current user and filter the query
    # inner join the badges -> badgeawards
    # filter only the current users badges
    if current_user_only:
        current_user = request.user.pk
        q = Badges.objects.exclude(badgeawards__userId__badgeawards__isnull=True)
        q3 = q.filter(badgeawards__userId=current_user)

    else:
        q3 = Badges.objects.all()

    # q3 = q.filter(badgeawards__userId=current_user)
    # Create a dict of category levels and counts used in custom_tags
    badge_counts = {}
    for badge_cat in q3:
        if not badge_counts.has_key(badge_cat.levels):
            badge_counts[badge_cat.levels] = {
                'item': badge_cat.levels,
                'count': 0
            }

        badge_counts[badge_cat.levels]['count'] += 1

    player_rating = 0
    try:
        player_rating += badge_counts['G']['count'] * 100
    except:
        pass
    try:
        player_rating += badge_counts['S']['count'] * 50
    except:
        pass
    try:
        player_rating += badge_counts['B']['count'] * 25
    except:
        pass
    try:
        player_rating += badge_counts['M']['count'] * 25
    except:
        pass

    # Get a list of User
    q = UserMember.objects.all()

    # Get Lists of all urls for each section
    merit_badge_urls = q3.filter(levels='M')
    bronze_badge_urls = q3.filter(levels='B')
    silver_badge_urls = q3.filter(levels='S')
    gold_badge_urls = q3.filter(levels='G')
    # chuck it all in some context dictionaries for the render object
    context_dict = {'badgecounts': badge_counts, 'bronzebadges': bronze_badge_urls, 'silverbadges': silver_badge_urls,
                    'goldbadges': gold_badge_urls, 'meritbadges': merit_badge_urls, 'playerrating': player_rating, 'users': q}
    return context_dict


def get_badge_dictionaries_categories(request, current_user_only):
    # get the current user and filter the query
    # inner join the badges -> badgeawards
    # filter only the current users badges
    if current_user_only:
        current_user = request.user.pk
        q = Badges.objects.exclude(badgeawards__userId__badgeawards__isnull=True)
        q3 = q.filter(badgeawards__userId=current_user)

    else:
        q3 = Badges.objects.all()

    # q3 = q.filter(badgeawards__userId=current_user)
    # Create a dict of category levels and counts used in custom_tags
    badge_counts = {}
    for badge_cat in q3:
        if not badge_counts.has_key(badge_cat.category):
            badge_counts[badge_cat.category] = {
                'item': badge_cat.category,
                'count': 0
            }
        badge_counts[badge_cat.category]['count'] += 1

    # Get Lists of all urls for each section
    technical_badge_urls = q3.filter(category='Technical')
    physical_badge_urls = q3.filter(category='Physical')
    social_badge_urls = q3.filter(category='Social')
    psychological_badge_urls = q3.filter(category='Psychological')
    # chuck it all in some context dictionaries for the render object
    context_dict = {'badgecounts': badge_counts, 'technicalbadges': technical_badge_urls, 'physicalbadges': physical_badge_urls,
                    'socialbadges': social_badge_urls, 'psychologicalbadges': psychological_badge_urls}
    return context_dict



def skills_matrix(request):
    response = render(request, 'member/skillsmatrix.html', {})
    return response


def attacking(request):
    response = render(request, 'member/skills/attacking.html', {})
    return response


# def kickups(request):
#     context_dictionary = get_badge_dictionaries_by_name(request, False)
#     response = render(request, 'member/skills/kickups.html', context_dictionary)
#     return response


def defending(request):
    response = render(request, 'member/skills/defending.html', {})
    return response


def teamwork(request):
    response = render(request, 'member/skills/teamwork.html', {})
    return response


def leadership(request):
    response = render(request, 'member/skills/leadership.html', {})
    return response


def technical(request):
    context_dict = get_badge_dictionaries_categories(request, False)
    response = render(request, 'member/technical.html', context=context_dict)
    return response


def social(request):
    context_dict = get_badge_dictionaries_categories(request, False)
    response = render(request, 'member/social.html', context=context_dict)
    return response


def physical(request):
    context_dict = get_badge_dictionaries_categories(request, False)
    response = render(request, 'member/physical.html', context_dict)
    return response


def psychological(request):
    context_dict = get_badge_dictionaries_categories(request, False)
    response = render(request, 'member/psychological.html', context_dict)
    return response


def kickups(request):
    badgeassessment_list = BadgeAssesments.objects.all()
    coach_instructions_list = CoachInstuction.objects.all()
    badge_dict_name_list = get_badge_dictionaries_by_name(request, False)
    context_dictionary =  {'badges': badge_dict_name_list, 'badgesassessments': badgeassessment_list, 'coachinstructions': coach_instructions_list}
    response = render(request, 'member/skills/kickups.html', context=context_dictionary)
    return response


def get_skill_page_by_uri(request):
    new_path = request.get_full_path()
    last_resource = basename(normpath(new_path))
    badgeassessment_list = BadgeAssesments.objects.all()
    coach_instructions_list = CoachInstuction.objects.all()
    coach_instructions_list = coach_instructions_list.filter(badgeName=last_resource)
    badge_dict_name_list = get_badge_dictionaries_by_name(request, False)
    context_dictionary =  {'badges': badge_dict_name_list, 'badgesassessments': badgeassessment_list, 'coachinstructions': coach_instructions_list}
    response = render(request, 'member/skills/skillpages.html', context=context_dictionary)
    return response


def add_member(request):
    form = UserMemberForm()

    if request.method == 'POST':
        form = UserMemberForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            print(form.errors)

    return render(request, 'member/add_member.html', {'form': form})


class ListContactView(ListView):
    model = Contact
    template_name = 'contact_list.html'


