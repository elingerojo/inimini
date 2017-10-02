from django.conf.urls import url
from sixerrapp import services, views, webhooks

urlpatterns = [
    # views.py
    url(r'^$', views.home, name='home'),
    url(r'^overview/$', views.overview, name='overview'),
    url(r'^privacy-policy/$', views.privacypolicy, name="privacypolicy"),
    url(r'^terms-of-use/$', views.termsofuse, name="termsofuse"),
    url(r'^my_gigs/$', views.my_gigs, name='my_gigs'),
    url(r'^create_gig/$', views.create_gig, name='create_gig'),
    url(r'^edit_gig/(?P<id>[0-9A-Fa-f-]+)/$', views.edit_gig, name='edit_gig'),
    url(r'^delete_gig/(?P<id>[0-9A-Fa-f-]+)/$', views.delete_gig, name='delete_gig'),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^validate_email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                                    views.validate_email, name='validate_email'),
    # webhooks.py
    url(r'^hook/$', webhooks.hook, name='hook'),
    # services.py
    url(r'^regions/$', services.get_json_data_by_key, name='get_json_data_by_key')
]
