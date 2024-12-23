from django.urls import path
from tourist_app import views
from django.conf.urls.static import static
from tourist_project import settings

urlpatterns = [
    path('home',views.home_view),
    path('packages',views.package_view),
    path('contact',views.contact_view),
    path('register',views.register_view),
    path('login',views.login_view),
    path('logout',views.logout_view),
    path('allpackages',views.allpackage_view),
    path('myjourney',views.journey_view),
    path('payment/<bid>',views.payment_view),
    path('makepayment',views.makepayment_view),
    path('remove/<jid>',views.remove_view),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)