from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', views.LoginView, name='login'),
    url(r'^accounts/logout/$', views.LogoutView, name='logout', kwargs={'next_page': '/'}),
    url(r'', include('blog.urls')),
]
