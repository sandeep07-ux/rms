from django.urls import path
from django.views.generic.base import RedirectView, View
from hotel import views
from django.contrib.auth import views as auth_views

from .views import KhaltiView
from .forms import LoginForm, PasswordChange, PasswordReset, SetPassword

urlpatterns = [

    path('khalti/', KhaltiView.as_view(), name="khalti"),
    # path('', views.home),
    # path("chart/", views.EditorChartView.as_view(), name="chart"),
    path('', views.ItemView.as_view(), name='home'),

    path("search/", views.search, name="search"),
    # path('product-detail/<int:pk>/', views.product_detail, name='product-detail'),
    path('item-detail/<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name="showcart"),
    path('pluscart/', views.plus_cart, name="pluscart"),
    path('minuscart/', views.minus_cart, name="minusscart"),
    path('removecart/', views.remove_cart, name="removecart"),

    path('buy/', views.buy_now, name='buy-now'),

    path('profile/', views.ProfileView.as_view(), name='profile'),

    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    # # path('changepassword/', views.change_password, name='changepassword'),

    path('menu/<slug:menu>/', views.menu, name='menuitem'),
    path('menu/', views.menu, name='menu'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),

    # # path('login/', views.login, name='login'),
    path('account/login/', auth_views.LoginView.as_view(template_name='hotel/login.html',
         authentication_form=LoginForm), name='login'),

    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='hotel/passwordchange.html',
         form_class=PasswordChange, success_url="/passwordchangedone/"), name='passwordchange'),

    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(
        template_name='hotel/passwordchangedone.html'), name='passwordchangedone'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='hotel/password_reset.html', form_class=PasswordReset), name='password_reset'),

    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='hotel/password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='hotel/password_reset_confirm.html', form_class=SetPassword), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='hotel/password_reset_complete.html'), name='password_reset_complete'),

    # path('registration/', views.customerregistration, name='customerregistration'),
    path('registration/', views.CustomerRegistrationView.as_view(),
         name='customerregistration'),
]
