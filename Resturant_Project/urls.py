from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import user_passes_test
from Base_App.views import *
from Base_App import views 

def is_admin(user):
    return user.is_superuser

admin.site.login = user_passes_test(is_admin, login_url='/login/')(admin.site.login)

urlpatterns = [
    path("admin/", admin.site.urls),  
    path('user/', user_profile, name='user_profile'),
    path("login/", login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("logout/get/", RedirectView.as_view(url="/", permanent=False), name="logout_get"),
    path("register/", register_view, name="register"),
    path('', views.HomeView, name='home'),  # ✅ FIXED: Removed .as_view()
    path('about/', AboutView, name='About'),
    path('menu/', MenuView, name='Menu'),
    path('menu/category/<int:category_id>/', menu_category, name='menu_category'),
    path('booktable/', BookTableView, name='Book_Table'),
    path('feedback/', FeedbackView, name='Feedback_Form'),
    path('submit_feedback/', submit_feedback, name='submit_feedback'),
    path('order/<int:item_id>/', OrderView, name='order_view'),
    path('upi-payment/<int:order_id>/', upi_payment_page, name='upi_payment_page'),
    path('order-confirmation/<int:order_id>/', OrderConfirmationView, name='order_confirmation'),
    path('mock-payment-success/<int:order_id>/', mock_payment_success, name='mock_payment_success'),  
    path('order-status/<int:order_id>/', order_status_page, name='order_status_page'),
    path('update-order-status/<int:order_id>/<str:status>/', update_order_status, name='update_order_status'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
