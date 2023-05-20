"""todoApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import settings, views
from django.contrib.auth import views as auth_views

from django.contrib.auth.forms import AuthenticationForm, UsernameField

from django import forms


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(
        widget=forms.TextInput(
            attrs={"data-testid": "username"}
        )
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"data-testid": "password"}
    )
)


urlpatterns = [
    path('todos/', include('todos.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path(
        'login/', auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=UserLoginForm,
        ),
        name='login',
    ),
    path('', views.index),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
