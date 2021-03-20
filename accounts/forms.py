import datetime
from django import forms
from .models import Profile

# (the actual value to be set on the model ,human-readable name)
Month_CHOICES = (
    ('1', 'January'),
    ('2', 'February'),
    ('3', 'March'),
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),
)


GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)


def day_choices():
    return [(d, d) for d in range(1, 32)]


def year_choices():
    return reversed([(r, r) for r in range(1900, datetime.date.today().year+1)])


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    month = forms.ChoiceField(choices=Month_CHOICES)
    day = forms.ChoiceField(choices=day_choices)
    year = forms.ChoiceField(choices=year_choices)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.month = self.cleaned_data['month']
        user.day = self.cleaned_data['day']
        user.year = self.cleaned_data['year']
        user.gender = self.cleaned_data['gender']
        date = str(user.year)+'-'+str(user.month)+'-'+str(user.day)
        Profile.objects.create(user=user, gender=user.gender,
                               birthday=date)
        user.save()
