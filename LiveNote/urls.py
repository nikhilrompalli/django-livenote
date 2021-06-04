"""LiveNote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from LNote import urls
import django.contrib.auth.urls
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from LNote import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^LiveNote/',include(urls)),
    url(r'^auth/', include(django.contrib.auth.urls)),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^$', auth_views.LoginView.as_view(template_name='login.html'), name='home'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='logged_out.html'), name='logout'),

]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
