from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class UserMember(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    SEX_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    gender = models.CharField(max_length=1, choices=SEX_CHOICES)
    user = models.OneToOneField(User)
    full_name = models.CharField(max_length=128, unique=True, null=True)
    favourite_player = models.CharField(max_length=128, null=True)
    favourite_team = models.CharField(max_length=128, null=True)
    birthdate = models.DateField()
    slug = models.SlugField(unique=True)
    CONSENT_CHOICES = ((True, 'Yes'), (False, 'No'))
    consent = models.NullBooleanField(choices=CONSENT_CHOICES,
                                      max_length=3,
                                      blank=True, null=True, default=True )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        super(UserMember, self).save(*args, **kwargs)

    def __str__(self):
        return '{0}'.format(self.user)


class Contact(models.Model):

    first_name = models.CharField(max_length=255, )
    last_name = models.CharField(max_length=255, )
    email = models.EmailField()

    def __str__(self):

        return ' '.join([
            self.first_name,
            self.last_name,
        ])


class Badges(models.Model):

    GOLD = 'G'
    SILVER = 'S'
    BRONZE = 'B'
    MERIT = 'M'
    BADGE_LEVELS = (
        (GOLD, 'Gold'),
        (SILVER, 'Silver'),
        (BRONZE, 'Bronze'),
        (MERIT, 'Merit'),
    )
    TECHNICAL = 'TECH'
    PSYCHOLOGICAL = 'PSYCHOLOGICAL'
    PHYSICAL = 'PHYSICAL'
    SOCIAL = 'SOCIAL'
    BADGE_CATEGORIES = (
        (TECHNICAL, 'Technical'),
        (PSYCHOLOGICAL, 'Psychological'),
        (PHYSICAL, 'Physical'),
        (SOCIAL, 'Social'),
    )
    name = models.CharField(max_length=128)
    category = models.CharField(max_length=255, choices=BADGE_CATEGORIES)
    levels = models.CharField(max_length=1, choices=BADGE_LEVELS)
    pageUrl = models.CharField(max_length=200)
    iconUrl = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Badges"

    def __str__(self):
        return self.name + " " + self.get_levels_display()


class BadgeAssesments(models.Model):

    badgeId = models.ForeignKey(Badges, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Badge Assessments"

    def __str__(self):
        return self.description


class BadgeAwards(models.Model):

    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    badgeId = models.ForeignKey(Badges, on_delete=models.CASCADE)
    dateAwarded = models.DateField()

    class Meta:
        unique_together = ('badgeId', 'userId',)
        verbose_name_plural = "Badge Awards"

    def calculateVotes(self):
        return BadgeAwards.objects.filter(choice=self).count()


class BadgeVideos(models.Model):
    badgeId = models.ForeignKey(Badges, on_delete=models.CASCADE)
    pageUrl = models.CharField(max_length=200)
    description = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Badge Videos"

    def __str__(self):
        return self.description


class CoachInstuction(models.Model):
    TIP = 'T'
    WARNING = 'W'
    INFO = 'I'
    INSTRUCTION_TYPE = (
        (TIP, 'Tip'),
        (WARNING, 'Warning'),
        (INFO, 'Info'),
    )
    badgeName = models.CharField(max_length=100)
    tipType = models.CharField(max_length=1, choices=INSTRUCTION_TYPE)
    description = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Coach Instructions"

    def __str__(self):
        return self.badgeName
