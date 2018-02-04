''' cutsom forms for the accounts application '''

from django import forms
from django.contrib.auth.forms import (UserCreationForm,
                                       PasswordChangeForm)
from django.contrib.auth.models import User

from accounts.models import UserProfile

class SignUpForm(UserCreationForm):
    ''' extends the built-in user creation form, so as to add in our extra data '''
    date_of_birth = forms.DateTimeField(label='Date of Birth',
                                        input_formats=['%Y-%m-%d',
                                                       '%m/%d/%Y',
                                                       '%d/%m/%y'],
                                       )
    bio = forms.CharField(max_length=300, min_length=10)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'date_of_birth',
            'bio',
        )

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(SignUpForm, self).save(commit=True)
        user_profile = UserProfile(user=user,
                                   date_of_birth=self.cleaned_data['date_of_birth'],
                                   bio=self.cleaned_data['bio'],
                                   avatar=self.cleaned_data['avatar'])
        print(user_profile.avatar)
        user_profile.save()
        return user, user_profile


class EditProfileForm(forms.ModelForm):
    ''' form to allow changes to the UserProfile '''
    bio = forms.CharField(max_length=300, min_length=10)
    class Meta:
        model = UserProfile
        fields = (
            'bio',
            'avatar',
        )

class UserUpdateForm(forms.ModelForm):
    """Form for updating user basic information."""
    verify_email = forms.EmailField(label="Please verify your email address.")

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'verify_email',
                 )

    def clean(self):
        email = self.cleaned_data.get('email')
        if email.has_changed():
            verify = self.cleaned_data.get('verify_email')
            if email != verify:
                raise forms.ValidationError(
                    "You need to enter the same email in both fields"
                )
