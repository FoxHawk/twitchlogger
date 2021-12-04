"""twitchStreamLogger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls.conf import re_path
from django.views.generic.base import RedirectView
from django.conf import settings

favicon_view = RedirectView.as_view(url=settings.STATIC_URL + "favicon.ico", permanent=True)

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', include('frontend.urls')),
	path('logger/', include("twitchEvents.urls")),
	path('api/', include("api.urls")),
	re_path("favicon.ico", favicon_view),
]
