from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('Profile/',views.profile,name='profile'),
    path('contact/',views.contact,name='contact'),
    
    # product
    path('updateItem/',views.updateItem,name='updateItem'),
    path('product/<int:pk>/',views.product_view,name='product'),
    
    # cart & checkout
    path('checkout/',views.checkout,name='checkout'),
    path('order/',views.orders,name='order'),
    path('cart/',views.cart,name='cart'),
    path('addCart/<int:pk>',views.addCart,name='addCart'),
    path('placeOrder/<int:pk>',views.placeOrder,name='placeOrder'),

    # Authentication
    path('singin/',views.signInPage,name='signin'),
    path('signup/',views.signUpPage,name='signup'),
    path('logout/',views.logoutUser,name='logout'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)