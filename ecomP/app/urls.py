from django.urls import path
from .views import *
app_name = 'app'
urlpatterns= [
    path('', HomeView.as_view(), name='home'),
    path('contact/', ContactView.as_view(), name='contacts'),
    path('about/', AboutView.as_view(), name='about'),
    
    path('categories/', AllProductsView.as_view(), name='categories'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='productdetails'),
    
    path('add-to-cart/<int:pro_id>/', AddToCartView.as_view(), name='addtocart'),
    path('my-cart/', MyCartView.as_view(), name='mycart'),
    path('manage-cart/<int:cp_id>/', ManageCartView.as_view(), name="managecart"),
    path('empty-cart/', EmptyCartView.as_view(), name='emptycart'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),

    path('register/', CustomerRegistration.as_view(), name="customerregistration"),
    
    path("logout/", CustomerLogoutView.as_view(), name="customerlogout"),
    path('login/', CustomerLoginView.as_view(), name="customerlogin"),
]
