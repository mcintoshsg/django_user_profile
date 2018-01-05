''' accounts specific urls
    urls for the accounts application '''

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^sign_in/$', views.sign_in, name='sign_in'),
    url(r'sign_up/$', views.sign_up, name='sign_up'),
    url(r'sign_out/$', views.sign_out, name='sign_out'),
    url(r'view_profile/$', views.view_profile, name='view_profile'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'edit_profile/$', views.edit_profile, name='edit_profile'),
]
