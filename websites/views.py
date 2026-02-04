from django.shortcuts import get_object_or_404, redirect, render
from websites import models
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        User.objects.create_user(username=username, email=email, password=password)
        return redirect("login")

    return render(request, "signup.html")

def login_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def logout_page(request):
    logout(request)
    return redirect("/")

@login_required(login_url="/login/")
def index(request):
    slider_data = models.SliderModel.objects.all()
    features_data = models.FeaturesModel.objects.all()
    products_data = models.productsmodel.objects.all()
    about_data = models.AboutSectionhomeModel.objects.last()
    Testimonial_data = models.TestimonialsModel.objects.all()

    packet = {
        'slider_data': slider_data,
        'features_data': features_data,
        'products_data': products_data,
        'about_data': about_data,
        'Testimonial_data': Testimonial_data,
    }
    return render(request, 'index.html', packet)

def products(request):
    all_products = models.Product.objects.all()
    return render(request, 'products.html', {"products": all_products})

def product_details(request, slug):
    product = get_object_or_404(models.Product, slug=slug)
    return render(request, 'product_details.html', {"product": product})

def add_to_cart(request, slug):
    product = get_object_or_404(models.Product, slug=slug)

    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_item, created = models.CartItem.objects.get_or_create(
        product=product,
        session_key=session_key,
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_page')

def cart_page(request):
    session_key = request.session.session_key
    items = models.CartItem.objects.filter(session_key=session_key)

    total = sum(i.subtotal() for i in items)

    return render(request, "cart.html", {"items": items, "total": total})

@login_required(login_url="/login/")
def checkout(request):
    session_key = request.session.session_key
    items = models.CartItem.objects.filter(session_key=session_key)
    total = sum(i.subtotal() for i in items)
    
    if not items.exists():
        messages.warning(request, "Your cart is empty")
        return redirect('cart_page')
    
    # Razorpay setup
    razorpay_order_id = None
    razorpay_key = None
    
    if total > 0:
        try:
            # Check if Razorpay keys are configured
            if hasattr(settings, 'RAZORPAY_KEY_ID') and hasattr(settings, 'RAZORPAY_KEY_SECRET'):
                if settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET:
                    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                    
                    # Create Razorpay order
                    razorpay_order = client.order.create({
                        "amount": int(total * 100),  # Convert to paise
                        "currency": "INR",
                        "payment_capture": "1",
                        "notes": {
                            "user_id": str(request.user.id),
                            "session_key": session_key
                        }
                    })
                    
                    razorpay_order_id = razorpay_order["id"]
                    razorpay_key = settings.RAZORPAY_KEY_ID
        except Exception as e:
            print(f"Razorpay error in checkout: {e}")
            # Continue without Razorpay

    return render(request, "checkout.html", {
        "items": items,
        "total": total,
        "razorpay_key": razorpay_key,
        "razorpay_order_id": razorpay_order_id,
    })

@login_required(login_url="/login/")
def place_order(request):
    """Cash on Delivery ऑर्डरसाठी"""
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        payment_method = request.POST.get("payment_method", "cod")

        session_key = request.session.session_key
        items = models.CartItem.objects.filter(session_key=session_key)
        
        if not items.exists():
            messages.error(request, "Your cart is empty")
            return redirect('cart_page')
            
        total = sum(i.subtotal() for i in items)

        # Create Order
        order = models.Order.objects.create(
            user=request.user,
            name=name,
            phone=phone,
            address=address,
            total_amount=total,
            payment_method=payment_method,
            payment_status="pending" if payment_method == "cod" else "paid"
        )

        # Create Order Items
        for item in items:
            models.OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear Cart
        items.delete()

        return redirect('payment_success')
    
    # GET request असल्यास checkout page वर पाठवा
    return redirect('checkout')

@login_required(login_url="/login/")
def place_order_cod(request):
    """विशेष COD ऑर्डर फंक्शन"""
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        session_key = request.session.session_key
        items = models.CartItem.objects.filter(session_key=session_key)
        
        if not items.exists():
            messages.error(request, "Your cart is empty")
            return redirect('cart_page')
            
        total = sum(i.subtotal() for i in items)

        # Create Order
        order = models.Order.objects.create(
            user=request.user,
            name=name,
            phone=phone,
            address=address,
            total_amount=total,
            payment_method="cod",
            payment_status="pending"
        )

        # Create Order Items
        for item in items:
            models.OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear Cart
        items.delete()

        return redirect('payment_success')
    
    return redirect('checkout')

@login_required(login_url="/login/")
def payment_success(request):
    """Payment success page - सोपी आवृत्ती"""
    
    # GET parameter मधून payment_id घ्या
    payment_id = request.GET.get('payment_id')
    
    # सर्वात शेवटचा ऑर्डर शोधा
    order = models.Order.objects.filter(user=request.user).last()
    
    if not order:
        messages.info(request, "No order found. Please place an order first.")
        return redirect('products')
    
    # जर payment_id असेल तर ते save करा
    if payment_id and not order.razorpay_payment_id:
        order.razorpay_payment_id = payment_id
        order.payment_method = 'online'
        order.payment_status = 'paid'
        order.save()
    
    return render(request, "payment_success.html", {"order": order})

@csrf_exempt
@login_required(login_url="/login/")
def razorpay_callback(request):
    """Razorpay payment callback"""
    if request.method == "POST":
        try:
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_signature = request.POST.get('razorpay_signature')
            name = request.POST.get('name', '')
            phone = request.POST.get('phone', '')
            address = request.POST.get('address', '')
            
            # Verify payment signature
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            
            # Verify signature
            client.utility.verify_payment_signature(params_dict)
            
            # Get cart items
            session_key = request.session.session_key
            items = models.CartItem.objects.filter(session_key=session_key)
            total = sum(i.subtotal() for i in items)
            
            if not items.exists():
                # If cart is empty, check if we have the order already
                try:
                    order = models.Order.objects.get(
                        razorpay_order_id=razorpay_order_id,
                        user=request.user
                    )
                    return redirect('payment_success')
                except models.Order.DoesNotExist:
                    messages.error(request, "Your cart is empty")
                    return redirect('cart_page')
            
            # Create Order
            order = models.Order.objects.create(
                user=request.user,
                name=name if name else request.user.get_full_name() or request.user.username,
                phone=phone if phone else "Online Payment",
                address=address if address else "Online Payment",
                total_amount=total,
                payment_method="online",
                payment_status="paid",
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_id=razorpay_payment_id,
                razorpay_signature=razorpay_signature,
                status="placed"
            )
            
            # Create Order Items
            for item in items:
                models.OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            
            # Clear Cart
            items.delete()
            
            # Redirect to success page
            return redirect('payment_success')
            
        except razorpay.errors.SignatureVerificationError:
            messages.error(request, "Payment verification failed")
            return redirect('checkout')
        except Exception as e:
            print(f"Payment error: {e}")
            messages.error(request, f"Payment error: {str(e)}")
            return redirect('checkout')
    
    return redirect('checkout')

def update_cart(request, product_id, action):
    """Update cart quantity"""
    session_key = request.session.session_key
    try:
        cart_item = models.CartItem.objects.get(
            product_id=product_id,
            session_key=session_key
        )
        
        if action == "plus":
            cart_item.quantity += 1
            cart_item.save()
        elif action == "minus":
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        
        return JsonResponse({
            "status": "ok", 
            "quantity": cart_item.quantity,
            "subtotal": cart_item.subtotal()
        })
    except models.CartItem.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Item not found"})

@login_required(login_url="/login/")
def track_order(request, order_id):
    order = get_object_or_404(models.Order, id=order_id, user=request.user)
    return render(request, "track_order.html", {"order": order})

@login_required(login_url="/login/")
def track_status_api(request, order_id):
    order = get_object_or_404(models.Order, id=order_id, user=request.user)
    return JsonResponse({"status": order.status})

@login_required(login_url="/login/")
def dashboard(request):
    user = request.user
    orders = models.Order.objects.filter(user=user).order_by("-id")
    return render(request, "dashboard.html", {"user": user, "orders": orders})

@login_required(login_url="/login/")
def my_orders(request):
    orders = models.Order.objects.filter(user=request.user).order_by("-id")
    return render(request, "my_orders.html", {"orders": orders})

def cart_count(request):
    """Get cart item count"""
    session_key = request.session.session_key
    count = models.CartItem.objects.filter(session_key=session_key).count()
    return JsonResponse({"count": count})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def farmer_registration(request):
    return render(request, 'farmer_registration.html')