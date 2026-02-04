from django.contrib import admin
from django.urls import path
from websites import views as web

urlpatterns = [
    path("signup/", web.signup, name="signup"),
    path("login/", web.login_page, name="login"),
    path("logout/", web.logout_page, name="logout"),
    path('', web.index, name='index'),
    path('about/', web.about, name='about'),
    path('products/', web.products, name='products'),
    path('product/<slug:slug>/', web.product_details, name='product_details'),
    path("cart/", web.cart_page, name="cart_page"),
    path("add-to-cart/<slug:slug>/", web.add_to_cart, name="add_to_cart"),
    
    # Checkout & Payment URLs
    path("checkout/", web.checkout, name="checkout"),
    path("place_order/", web.place_order, name="place_order"),
    path("place_order-cod/", web.place_order_cod, name="place_order_cod"),
    path("razorpay-callback/", web.razorpay_callback, name="razorpay_callback"),
    
    # Payment Success URL (हायफनसह)
    path("payment-success/", web.payment_success, name="payment_success_hyphen"),
    
    # Order Tracking URLs
    path("track/<int:order_id>/", web.track_order, name="track_order"),
    path("track-status/<int:order_id>/", web.track_status_api, name="track_status_api"),
    
    # Cart Management
    path("update_cart/<int:product_id>/<str:action>/", web.update_cart, name="update_cart"),
    path("cart_count/", web.cart_count, name="cart_count"),
    
    # Other Pages
    path('contact/', web.contact, name='contact'),
    path('farmer_registration/', web.farmer_registration, name='farmer_registration'),
    
    # Dashboard
    path("dashboard/", web.dashboard, name="dashboard"),
    path("my_orders/", web.my_orders, name="my_orders"),
    
        # Payment URLs
    path("checkout/", web.checkout, name="checkout"),
    path("razorpay-callback/", web.razorpay_callback, name="razorpay_callback"),
    path("payment-success/", web.payment_success, name="payment_success"),
    path("place_order-cod/", web.place_order_cod, name="place_order_cod"),
        # दोन्ही versions जोडा
    path("my-orders/", web.my_orders, name="my_orders_hyphen"),
    path("my_orders/", web.my_orders, name="my_orders"),
    # Admin
    path('admin/', admin.site.urls),
]