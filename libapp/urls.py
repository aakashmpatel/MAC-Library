from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^about$', views.about, name='about'),
        url(r'^detail/(?P<item_id>\d+)/$', views.detail, name='detail'),
        url(r'^newitem$',views.newitem,name='newitem'),
        url(r'^suggestions$',views.suggestions,name='suggestions'),
        url(r'^search$',views.searchlib,name='search'),
        url(r'^login$',views.user_login,name='login'),
        url(r'^register$',views.register,name='register'),
        url(r'^logout$',views.user_logout,name='logout'),
        url(r'^myitems$',views.myitems,name='myitems'),
        url(r'^info/(?P<item_id>\d+)/$',views.info,name='info')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
