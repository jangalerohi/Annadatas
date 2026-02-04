from websites.models import OrderItem

def cart_count(request):
    if request.user.is_authenticated:
        return {"cart_count": OrderItem.objects.filter(order__user=request.user).count()}
    return {"cart_count": 0}
