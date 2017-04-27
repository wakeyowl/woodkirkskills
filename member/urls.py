from django.conf.urls import url

import member
from member import views

urlpatterns = [
    # Basepage URL
    url(r'^$', views.skills_matrix, name='skillsmatrix'),
    # Skill Sections Urls
    url(r'^skillsmatrix/technical/firsttouch/$', views.get_skill_page_by_uri, name='skillpages'),
    url(r'^skillsmatrix/technical/goalkeeper/$', views.get_skill_page_by_uri, name='skillpages'),
    url(r'^skillsmatrix/technical/passing/$', views.get_skill_page_by_uri, name='skillpages'),
    url(r'^skillsmatrix/psychological/kickups/$', views.get_skill_page_by_uri, name='skillpages'),
    url(r'^skillsmatrix/psychological/toetaps/$', views.get_skill_page_by_uri, name='skillpages'),
    url(r'^skillsmatrix/social/attacking/$', views.get_skill_page_by_uri, name='skillpages'),
    url(r'^skillsmatrix/social/defending/$', views.get_skill_page_by_uri, name='skillpages'),
    url(r'^skillsmatrix/physical/dribbling/$', views.get_skill_page_by_uri, name='skillpages'),
    url(r'^skillsmatrix/physical/heading/$', views.get_skill_page_by_uri, name='skillpages'),
    url(r'^skillsmatrix/social/leadership/$', views.leadership, name='leadership'),
    url(r'^skillsmatrix/social/teamwork/$', views.teamwork, name='teamwork'),
    # Menu URLs
    url(r'^mybadges/$', views.mybadges, name='mybadges'),
    url(r'^allbadges/$', views.allbadges, name='allbadges'),
    url(r'^skillsmatrix/$', views.skills_matrix, name='skillsmatrix'),
    url(r'^skillsmatrix/challengebadges/$', views.challengebadges, name='challengebadges'),
    url(r'^skillsmatrix/technical/$', views.technical, name='technical'),
    url(r'^skillsmatrix/social/$', views.social, name='social'),
    url(r'^skillsmatrix/psychological/$', views.psychological, name='psychological'),
    url(r'^skillsmatrix/physical/$', views.physical, name='physical'),
    # Registration URLs
    url(r'^add_member/$', views.add_member, name='add_member'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),

]
