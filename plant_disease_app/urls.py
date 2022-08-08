from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home,name='home'),
    path('home/',home,name='home'),
    path('login-h/', loginpage, name="login-h"),
    path('register/', register, name="register"),
    path('logout-h/', logoutUser, name="logout-h"),
    path('photo/',photo_store,name='photo'),
    path('check/',check,name='check'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)