"""
URL configuration for rateyourseat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from app_inicial.views import home, log_in, sign_up, log_out, add_review, my_reviews, reviews, single_review
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('home/', home),
    path('log_in/', log_in),
    path('sign_up/', sign_up),
    path('log_out/', log_out, name='logout'),
    path('add-review/', add_review, name='add-review'),
    path('reviews/', reviews, name='reviews'),
    path('my_reviews/', my_reviews, name='my_reviews'),
    path('single_review/<str:id>', single_review, name='single_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
