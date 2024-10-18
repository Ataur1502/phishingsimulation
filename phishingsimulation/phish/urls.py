from django.urls import path
from .views import index,signin,signup,activate,home,logout_view,phishing,simshing,SpearPhishing,Whaling,trigger_simulation,real_link,fake_phishing_link
urlpatterns=[
    path("",index,name="index"),
    path("signin/",signin ,name="signin"),
    path("signup/",signup ,name="signup"),
    path("home",home, name='home'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'),
    path('logout/',logout_view, name='logout'),
    path('phishing/',phishing, name='phishing'),
    path('simshing/',simshing, name='simshing'),
    path('spearphishing/',SpearPhishing, name='spearphishing'),
    path('whaling/',Whaling, name='Whaling'),
    path('stimulate/',trigger_simulation,name='trigger_simulation'),
    path('real/', real_link, name='real'),                
    path('fake/', fake_phishing_link, name='fake'),
]