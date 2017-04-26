from django.conf.urls import url

import member
from member import views

urlpatterns = [
    url(r'^$', views.skills_matrix, name='skillsmatrix'),
    url(r'^mybadges/$', views.mybadges, name='mybadges'),
    url(r'^allbadges/$', views.allbadges, name='allbadges'),
    url(r'^skillsmatrix/$', views.skills_matrix, name='skillsmatrix'),
    url(r'^skills_matrix/challengebadges/$', views.challengebadges, name='challengebadges'),
    url(r'^skills_matrix/technical/$', views.technical, name='technical'),
    url(r'^skills_matrix/social/$', views.social, name='social'),
    url(r'^skills_matrix/social/attacking/$', views.attacking, name='attacking'),
    url(r'^skills_matrix/social/leadership/$', views.leadership, name='leadership'),
    url(r'^skills_matrix/social/teamwork/$', views.teamwork, name='teamwork'),
    url(r'^skills_matrix/social/defending/$', views.defending, name='defending'),
    url(r'^skills_matrix/psychological/$', views.psychological, name='psychological'),
    url(r'^skills_matrix/psychological/kickups/$', views.kickups, name='kickups'),
    url(r'^skills_matrix/physical/$', views.physical, name='physical'),
    url(r'^add_member/$', views.add_member, name='add_member'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),

]
