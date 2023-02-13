from store.forms import LoginForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'store'


urlpatterns = [
    path('',views.firstone,name='firstone'),
    path('new/', views.new, name="new"),
    path('index',views.home,name='home'),


    #staff
    # path('stafflogin/',views.stafflogin,name='stafflogin'),
    path('staffloginaction/',views.staffloginaction,name='staffloginaction'),
    path('staffhome/',views.staffhome,name='staffhome'),
    path('addproduct/',views.addproducts,name='addproducts'),
    path('view orderdetails/<int:id>/',views.staffvieworderdetails,name='staffvieworderdetails'),
    path('updateorder/<int:id>/',views.staffupdateorder,name='staffupdateorder'),
    path('sendmail/',views.inform,name='inform'),
    path('viewfeedback/',views.staffviewfeedback,name='staffviewfeedback'),
    path('viewcontact/',views.staffviewcontact,name='staffviewcontact'),
    path('viewrationcard/',views.staffviewrationcard,name='staffviewrationcard'),
    path('takeorder/',views.stafftakeorder,name='stafftakeorder'),
    path('viewcustomerdetail/',views.staffviewcustomer,name='staffviewcustomer'),
    path('addreport/',views.staffaddreport,name='staffaddreport'),
    path('viewreview/',views.staffviewreview,name='staffviewreview'),



    path('addstock/',views.staffaddstock,name='staffaddstock'),
    # URL for Cart and Checkout


    path('addfeedback/',views.customeraddfeedback,name='customeraddfeedback'),
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('remove-cart/<int:cart_id>/', views.remove_cart, name="remove-cart"),
    path('plus-cart/<int:cart_id>/', views.plus_cart, name="plus-cart"),
    path('minus-cart/<int:cart_id>/', views.minus_cart, name="minus-cart"),
    path('cart/', views.cart, name="cart"),
    path('save-review/<int:pid>', views.save_review, name='save-review'),
    path('subseedyproduct/', views.getsubseedycat, name='getsubseedycat'),
    path('nosubseedyproduct/',views.getnosubseedycat,name='getnosubseedycat'),
    path('checkout/', views.checkout, name="checkout"),
    path('orders/', views.orders, name="orders"),
    path('orderview/<int:id>',views.orderdetail,name='orderdetail'),
    path('details/',views.customerviewdetails,name='customerviewdetails'),
    path('payment/',views.paymentview,name='paymentview'),
    path('addreview/',views.customeraddreview,name='customeraddreview'),


    #URL for Products
    path('product/<slug:slug>/', views.detail, name="product-detail"),
    path('categories/', views.all_categories, name="all-categories"),
    path('<slug:slug>/', views.category_products, name="category-products"),

    path('shop/', views.shop, name="shop"),

    # URL for Authentication
    path('accounts/register/', views.RegistrationView.as_view(), name="register"),
    path('accounts/login/', views.LoginView.as_view(), name="login"),
    path('accounts/profile/', views.profile, name="profile"),

    path('accounts/add-address/',views.AddressView.as_view(), name="add-address"),
    path('accounts/remove-address/<int:id>/', views.remove_address, name="remove-address"),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='store:login'), name="logout"),

    path('accounts/password-change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change.html', form_class=PasswordChangeForm, success_url='/accounts/password-change-done/'), name="password-change"),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name="password-change-done"),

    path('accounts/password-reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html', form_class=PasswordResetForm, success_url='/accounts/password-reset/done/'), name="password-reset"), # Passing Success URL to Override default URL, also created password_reset_email.html due to error from our app_name in URL
    path('accounts/password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name="password_reset_done"),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html', form_class=SetPasswordForm, success_url='/accounts/password-reset-complete/'), name="password_reset_confirm"), # Passing Success URL to Override default URL
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name="password_reset_complete"),



    
]
