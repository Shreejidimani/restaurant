"""
URL configuration for Resturant_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from Base_App import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import user_passes_test
from Base_App.views import *

def is_admin(user):
    return user.is_superuser

admin.site.login = user_passes_test(is_admin, login_url='/login/')(admin.site.login)
urlpatterns = [
    path("admin/", admin.site.urls),  # Admin Panel
    path('user/', user_profile, name='user_profile'),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("logout/get/", RedirectView.as_view(url="/", permanent=False), name="logout_get"),
    path("register/", views.register_view, name="register"),
    path('admin/', admin.site.urls),
    path("", HomeView, name="Home"),
    path('about/', AboutView, name='About'),
    path('menu/', MenuView, name='Menu'),
    path('menu/category/<int:category_id>/', views.menu_category, name='menu_category'),
    path('booktable/', BookTableView, name='Book_Table'),
    path('feedback/', FeedbackView, name='Feedback_Form'),
    path('submit_feedback/', submit_feedback, name='submit_feedback'),
    path('order/<int:item_id>/', OrderView, name='order_view'),
    path('upi-payment/<int:order_id>/', upi_payment_page, name='upi_payment_page'),
    path('order-confirmation/<int:order_id>/', OrderConfirmationView, name='order_confirmation'),
    path('mock-payment-success/<int:order_id>/', mock_payment_success, name='mock_payment_success'),  
    path('order-status/<int:order_id>/', views.order_status_page, name='order_status_page'),
    path('update-order-status/<int:order_id>/<str:status>/', views.update_order_status, name='update_order_status'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)