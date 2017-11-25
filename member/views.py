from datetime import datetime

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Max, Min
from os.path import normpath, basename

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.views.generic import ListView
from registration.backends.simple.views import RegistrationView
from django.contrib import messages

from member.forms import UserMemberForm, UserMemberUpdateForm, PlayerBattleForm
from member.models import UserMember, Contact, Badges, BadgeAssesments, BadgeMedia, CoachInstuction, BadgeAwards, \
    PlayerMatchAwards, TeamManagers, User


class WoodkirkRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('register_profile')

player_awards = {}


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


def player_battles_menu(request, template_name='member/player_battle_form.html'):
        form = PlayerBattleForm()

        if request.GET.get('featured'):
            featured_filter = request.GET.get('featured')
            listings = TeamManagers.objects.filter(featured_choices=featured_filter)
        else:
            listings = TeamManagers.objects.all()

        if request.method == 'POST':
            form = PlayerBattleForm(request.POST)

            if form.is_valid():

                # Grab the user and challenged player for the data filter query
                current_user=request.user.pk
                # current_user2 = get_object_or_404(BadgeAwards, userId_id=request.user.pk)
                challenged_player = form.cleaned_data['player_to_battle'].user_id
                return player_battles(request, current_user, challenged_player)
            else:
                print(form.errors)

        context_dict = {'listings': listings}

        return render(request, template_name, {'form': form}, context_dict)


def player_battles(request, current_user_id, challenged_player_id):

    # Get all badge Awards
    q = BadgeAwards.objects.all()
    # query filter just the current users badges
    qcurrent = q.filter(userId_id=current_user_id)
    max = qcurrent.aggregate(Max('score'))
    min = qcurrent.aggregate(Min('score'))
    # create a seperate query filter for challenges
    qchallenged = q.filter(userId_id=challenged_player_id)

    context_dict = {'current_player': qcurrent, 'challenged_player': qchallenged}
    response = render(request, 'member/playerbattles.html', context_dict)
    return response


def update_user(request):
    userupdated = get_object_or_404(UserMember, user=request.user.pk)
    if request.method == "POST":
        form = UserMemberUpdateForm(request.POST, request.FILES, instance=userupdated)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            post.save()
            return redirect('mybadges', )
    else:
        form = UserMemberUpdateForm(instance=userupdated)

    return render(request, 'member/usermember_update_form.html', {'form': form})


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
    badge_videos = BadgeMedia.objects.all()
    context_dict = {'badgecounts': badge_counts, 'merit': meritbadge_list, 'meritassessments': badgeassessment_list,
                    'badgevideos': badge_videos}
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


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile', )
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


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
    global player_awards
    current_user = request.user.pk
    if current_user_only:

        q = Badges.objects.exclude(badgeawards__userId__badgeawards__isnull=True)
        q3 = q.filter(badgeawards__userId=current_user)
        # Get the PlayerMatchAwards
        matchAwards = PlayerMatchAwards.objects.all()
        matchAwards = matchAwards.filter(userId_id=current_user)
        player_awards = {
            'goals': 0,
            'potm': 0,
            'clean_sheets': 0
        }
        for award in matchAwards:
            if (award.awardType == 'POTMS'):
                player_awards['potm'] += award.score
            elif (award.awardType == 'GOALS'):
                player_awards['goals'] += award.score
            elif (award.awardType == 'CLEANSHEETS'):
                player_awards['clean_sheets'] += award.score

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


    curr_user = UserMember.objects.all()
    curr_user = curr_user.filter(user_id=current_user)

    # Get Lists of all urls for each section
    merit_badge_urls = q3.filter(levels='M')
    bronze_badge_urls = q3.filter(levels='B')
    silver_badge_urls = q3.filter(levels='S')
    gold_badge_urls = q3.filter(levels='G')

    # Get Badge Award History using select_related to get badge info also on FK's
    badge_awards_list = BadgeAwards.objects.all()
    badge_awards_list = badge_awards_list.filter(userId_id=current_user)
    badge_awards_list = badge_awards_list.select_related().order_by('-dateAwarded')

    # Get Percentages
    badgedata = get_percentages_of_categories(request)




    # chuck it all in some context dictionaries for the render object
    context_dict = {'badgecounts': badge_counts, 'bronzebadges': bronze_badge_urls, 'silverbadges': silver_badge_urls,
                    'goldbadges': gold_badge_urls, 'meritbadges': merit_badge_urls, 'playerrating': player_rating,
                    'users': q, 'badgedata': badgedata, 'badge_awards': badge_awards_list, 'player_awards': player_awards, 'current_user': curr_user}
    return context_dict


def get_percentages_of_categories(request):
    player_totals = Badges.objects.all()
    current_user = request.user.pk
    player_totals = Badges.objects.exclude(badgeawards__userId__badgeawards__isnull=True)
    player_totals = player_totals.filter(badgeawards__userId=current_user)
    # Get the total of each category
    badge_counts = {}
    for badge_cat in player_totals:
        if not badge_counts.has_key(badge_cat.levels):
            badge_counts[badge_cat.levels] = {
                'item': badge_cat.levels,
                'count': 0
            }

        badge_counts[badge_cat.levels]['count'] += 1
    player_merit_badge_count = player_totals.filter(levels='M').count()
    player_bronze_badge_count = player_totals.filter(levels='B').count()
    player_silver_badge_count = player_totals.filter(levels='S').count()
    player_gold_badge_count = player_totals.filter(levels='G').count()
    player_all_badge_count = player_totals.filter().count()

    all_badge_totals = Badges.objects.all()
    all_merit_badge_count = all_badge_totals.filter(levels='M').count()
    all_bronze_badge_count = all_badge_totals.filter(levels='B').count()
    all_silver_badge_count = all_badge_totals.filter(levels='S').count()
    all_gold_badge_count = all_badge_totals.filter(levels='G').count()
    all_badge_count = all_badge_totals.filter().count()

    # Set the percentages
    allbadge_percent = 0
    bronze_percent = 0
    silver_percent = 0
    gold_percent = 0
    merit_percent = 0
    try:
        allbadge_percent = round((player_all_badge_count / float(all_badge_count)) * 100, 0)
    except:
        pass
    try:
        bronze_percent = round((player_bronze_badge_count / float(all_bronze_badge_count)) * 100, 0)
    except:
        pass
    try:
        silver_percent = round((player_silver_badge_count / float(all_silver_badge_count)) * 100, 0)
    except:
        pass
    try:
        gold_percent = round((player_gold_badge_count / float(all_gold_badge_count)) * 100, 0)
    except:
        pass
    try:
        merit_percent = round((player_merit_badge_count / float(all_merit_badge_count)) * 100, 0)
    except:
        pass

    categories_to_check = ['bronze', 'silver', 'gold', 'merit']

    percentages_of_categories = {}

    percentages_of_categories['bronze'] = {
        'total_badges_count': all_bronze_badge_count,
        'player_badges_count': player_bronze_badge_count,
        'player_completion_percent': bronze_percent
    }

    percentages_of_categories['silver'] = {
        'total_badges_count': all_silver_badge_count,
        'player_badges_count': player_silver_badge_count,
        'player_completion_percent': silver_percent
    }

    percentages_of_categories['gold'] = {
        'total_badges_count': all_gold_badge_count,
        'player_badges_count': player_gold_badge_count,
        'player_completion_percent': gold_percent
    }

    percentages_of_categories['merit'] = {
        'total_badges_count': all_merit_badge_count,
        'player_badges_count': player_merit_badge_count,
        'player_completion_percent': merit_percent
    }

    return percentages_of_categories


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
    context_dict = {'badgecounts': badge_counts, 'technicalbadges': technical_badge_urls,
                    'physicalbadges': physical_badge_urls,
                    'socialbadges': social_badge_urls, 'psychologicalbadges': psychological_badge_urls}
    return context_dict


def skills_matrix(request):
    response = render(request, 'member/skillsmatrix.html', {})
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


def get_skill_page_by_uri(request):
    new_path = request.get_full_path()
    last_resource = basename(normpath(new_path))
    badgeassessment_list = BadgeAssesments.objects.all()
    coach_instructions_list = CoachInstuction.objects.all()
    coach_instructions_list = coach_instructions_list.filter(badgeName=last_resource).order_by('tipType')
    badge_dict_name_list = get_badge_dictionaries_by_name(request, False)
    badge_videos = BadgeMedia.objects.all()
    context_dictionary = {'badges': badge_dict_name_list, 'badgesassessments': badgeassessment_list,
                          'coachinstructions': coach_instructions_list, 'badgevideos': badge_videos}
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
