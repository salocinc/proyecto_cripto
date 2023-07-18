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
from app_inicial.views import log_in, sign_up, log_out, my_documents, single_document, create_document, request_to, secret_keys, sign_document, download_document, verification
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', verification),
    path('log_in/', log_in),
    path('sign_up/', sign_up),
    path('log_out/', log_out, name='logout'),
    path('request_to/', request_to, name='request_to'),
    path('my_documents/', my_documents, name='my_documents'),
    path('single_document/<str:id>', single_document, name='single_document'),
    path('sign_document/<str:id>', sign_document, name='sign_document'),
    path('create_document/', create_document, name='create_document'),
    path('secret_keys/', secret_keys, name='secret_keys'),
    path('descargar/<int:doc_id>/', download_document, name='download_document'),
    path('verification/', verification, name='verification')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
