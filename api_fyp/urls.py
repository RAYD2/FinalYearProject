"""
URL configuration for api_fyp project.

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
from django.urls import path, include
from .apiapp import views
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [

    path("admin/", admin.site.urls),
    path("", views.home, name = "home"),
    path("login/", views.user_login, name = "login"),
    path("signup/", views.user_signup, name = "signup"),
    path("logout/", views.user_logout, name = "logout"),
    path("dashboard/<int:pk>/", views.dash_view, name = "dash_view"),
    path("patients/<int:pk>/", views.patients, name = "patients"),
    path("patients/add/<int:pk>/", views.patient_add_list, name = "patient_add_list"),
    path("patients/remove/<int:pk>/", views.patient_remove_list, name = "patient_remove_list"),
    path("patients/flag/<int:pk>/", views.patient_flag, name = "patient_flag"),
    path("patient_dashboard/<int:pk>/<int:p_pk>/", views.patient_dashboard, name = "patient_dashboard"),
    path("patient_dashboard/add_mri/<int:pk>/<int:p_pk>/", views.add_img, name = "add_img"),
    path("patient_dashboard/prediction_view/<int:pk>/<int:p_pk>/", views.prediction_view, name="prediction_view"),
    path("profile/<int:pk>/", views.profile, name = "profile"),
    # automatic creation of a url for image path
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT )
