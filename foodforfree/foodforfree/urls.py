from django.urls import path, include
from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('foods/', include('foods.urls')),
    path('admins/', include('admins.urls')),
    path('', include('accounts.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]


