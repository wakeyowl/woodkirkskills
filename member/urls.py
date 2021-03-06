from django.conf.urls import url

from member import views
from woodkirkvalleydata import settings
from django.conf.urls.static import static

urlpatterns = [
                  # Basepage URL
                  url(r'^$', views.skills_matrix, name='skillsmatrix'),
                  url(r'^password/$', views.change_password, name='change_password'),
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
                  url(r'^skillsmatrix/social/leadership/$', views.get_skill_page_by_uri, name='leadership'),
                  url(r'^skillsmatrix/social/teamwork/$', views.get_skill_page_by_uri, name='teamwork'),
                  # Menu URLs
                  url(r'^mybadges/$', views.mybadges, name='mybadges'),

                  url(r'^allbadges/$', views.allbadges, name='allbadges'),
                  url(r'^skillsmatrix/$', views.skills_matrix, name='skillsmatrix'),
                  url(r'^skillsmatrix/challengebadges/$', views.challengebadges, name='challengebadges'),
                  url(r'^skillsmatrix/technical/$', views.technical, name='technical'),
                  url(r'^skillsmatrix/social/$', views.social, name='social'),
                  url(r'^skillsmatrix/psychological/$', views.psychological, name='psychological'),
                  url(r'^skillsmatrix/physical/$', views.physical, name='physical'),
                  url(r'^register_profile/$', views.register_profile, name='register_profile'),
                  url(r'^update/$', views.update_user, name='update_user'),
                  # Registration URLs
                  url(r'^add_member/$', views.add_member, name='add_member'),
                  # Player Battles
                  url(r'^selectbattle/$', views.player_battles_menu, name='select_battle'),
                  url(r'^playerbattles/$', views.player_battles, name='player_battles'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
