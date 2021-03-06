from django import forms
from django.utils.safestring import mark_safe
from member.models import UserMember, TeamManagers


class UserMemberForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    consent = forms.NullBooleanField(help_text=mark_safe("By consenting you are agreeing to the following: "
                                                         "<ul> "
                                                         "<li>I agree to work hard at training </li>"
                                                         "<li>I agree to practice my skills </li>"
                                                         "</ul>"))
    birthdate = forms.DateField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = UserMember
        fields = ('full_name', 'favourite_player', 'favourite_team', 'birthdate', 'consent', 'gender', 'managerId')


class UserMemberUpdateForm(forms.ModelForm):
    class Meta:
        model = UserMember
        fields = ('full_name', 'picture', 'squad_number','favourite_player', 'favourite_team', 'birthdate', )


class PlayerBattleForm(forms.Form):

        player_to_battle = forms.ModelChoiceField(queryset=UserMember.objects.all())
