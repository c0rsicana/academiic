from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_request, logout_request, showHomepage, SiteConfigView, registration_view


urlpatterns = [
    path('', showHomepage, name='home'),
    path('site-config/', SiteConfigView.as_view(), name='configs'),
    path('login/', login_request, name='login'),
    path('accounts/login/', login_request, name='accounts/login'),
    path('reset-password', auth_views.PasswordResetView.as_view(template_name="core/reset_password.html"), name='reset_password'),
    path('reset-password-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="core/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset-password-done', auth_views.PasswordResetDoneView.as_view(template_name="core/password_reset_done.html"), name='password_reset_done'),
    path('reset-password-complete', auth_views.PasswordResetCompleteView.as_view(template_name="core/password_reset_complete.html"), name='password_reset_complete'),
    path('logout/', logout_request, name='logout'),
    path('signup/', registration_view, name='signup'),
]
