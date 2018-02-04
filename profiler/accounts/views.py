
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render


from accounts.forms import (SignUpForm,
                            EditProfileForm,
                            UserUpdateForm)                           
from accounts.models import UserProfile


def sign_in(request):
    ''' sign in view for the accounts app '''
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('accounts:view_profile')
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    ''' sign_up view for our accounts application '''
    form = SignUpForm()
    print(request.method)
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('accounts:view_profile'))
        else:
            print(form.error_messages)
            print(form.cleaned_data['password1'])
            print(form.cleaned_data['password2'])
    return render(request, 'accounts/sign_up.html', {'form': form})

@login_required
def sign_out(request):
    ''' sign out view for the accounts application '''
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))

@login_required
def view_profile(request):
    ''' user profile view for the accounts application '''
    profile = get_object_or_404(UserProfile, user=request.user)
    context = {'user': request.user, 'avatar': request.FILES, 'profile': profile}
    return render(request, 'accounts/view_profile.html', context)

@login_required
def edit_profile(request):
    ''' edit profile view for the accounts application '''
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST,
                                       request.FILES,
                                       instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('accounts:view_profile'))
        else:
            print('error occurred on form')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.userprofile)
        return render(request, 'accounts/edit_profile.html',
                      {'user_form': user_form,
                       'profile_form': profile_form
                      })

@login_required                      
def change_password(request):
    ''' a view to allow users to change their password '''
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('accounts:view_profile'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })