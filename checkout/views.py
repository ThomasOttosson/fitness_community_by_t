from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib import messages
import stripe
from .models import Cart, CartItem, Order, OrderItem
from fitness.models import ExercisePlan, NutritionPlan
from subscriptions.models import Subscription
from products.models import Product
from django.db.models import Q


# Create your views here.
@require_POST
@login_required
def add_to_cart(request, item_type, pk):  # add chosen item to cart
    print(f"Adding to cart: item_type={item_type}, pk={pk}")
    if item_type == 'exercise_plan':
        item = get_object_or_404(ExercisePlan, pk=pk)
    elif item_type == 'nutrition_plan':
        item = get_object_or_404(NutritionPlan, pk=pk)
    elif item_type == 'product':
        item = get_object_or_404(Product, pk=pk)
    else:
        messages.error(request, 'Invalid item type.')
        return redirect('home')
    try:
        qty = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        messages.error(request, 'Invalid quantity.')
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    if qty <= 0:
        messages.error(request, 'Quantity must be at least 1.')
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    cart, _ = Cart.objects.get_or_create(user=request.user)
    flt = Q(cart=cart)
    if item_type == 'exercise_plan':
        flt &= Q(exercise_plan=item)
    elif item_type == 'nutrition_plan':
        flt &= Q(nutrition_plan=item)
    else:
        flt &= Q(product=item)
    cart_item = CartItem.objects.filter(flt).first()
    if cart_item:
        cart_item.quantity += qty
        cart_item.save()
    else:
        data = {'cart': cart, 'quantity': qty, 'price_at_addition': item.price}
        if item_type == 'exercise_plan':
            data['exercise_plan'] = item
        elif item_type == 'nutrition_plan':
            data['nutrition_plan'] = item
        else:
            data['product'] = item
        cart_item = CartItem.objects.create(**data)
    name = (cart_item.get_item_object().name if item_type == 'product'
            else cart_item.get_item_object().title)
    messages.success(request, f"'{name}' added to cart.")
    return redirect('cart_detail')


@login_required
def cart_detail(request):  # show cart
    cart = getattr(request.user, 'cart', None)
    return render(request, 'registration/cart_detail.html', {'cart': cart})


@require_POST
@login_required
def update_cart_item(request, item_id):  # change cart quantity
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    qty = int(request.POST.get('quantity', 1))
    if qty <= 0:
        item.delete()
        messages.success(request, 'Item removed.')
    else:
        item.quantity = qty
        item.save()
        messages.success(request, 'Quantity updated.')
    return redirect('cart_detail')


@require_POST
@login_required
def remove_from_cart(request, item_id):  # remove cart item
    itm = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    name = itm.get_item_object()
    itm.delete()
    messages.success(request, f"'{name}' removed from cart.")
    return redirect('cart_detail')


@login_required
def checkout(request):  # start checkout with Stripe
    cart = getattr(request.user, 'cart', None)
    if not cart or not cart.items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart_detail')

    # Get the total in cents for Stripe
    total = int(cart.get_total_cost() * 100)

    try:
        # Create a payment intent with Stripe
        intent = stripe.PaymentIntent.create(
            amount=total,
            currency='usd',
            metadata={'cart_id': cart.id, 'user_id': request.user.id},
        )

        # Pass all necessary context to the template
        ctx = {
            'cart': cart,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
            'client_secret': intent.client_secret,
        }
        return render(request, 'registration/checkout.html', ctx)
    except Exception as e:
        messages.error(request, f'Payment setup failed: {str(e)}')
        return redirect('cart_detail')


@login_required
def order_confirmation(request):  # show payment status
    status = request.session.pop('payment_status', 'unknown')
    return render(request, 'registration/payment_success.html',
                  {'status': status})


@login_required
def payment_success(request):  # handle Stripe callbacks
    sid = request.GET.get('session_id')
    secret = request.GET.get('payment_intent_client_secret')
    if sid:
        try:
            sess = stripe.checkout.Session.retrieve(sid)
        except stripe.error.StripeError as exc:
            messages.error(request, f'Stripe error: {exc}')
            return redirect('home')
        if sess.payment_status == 'paid':
            user = request.user
            itype = sess.metadata.get('item_type')
            iid = sess.metadata.get('item_id')
            plan = None
            if itype == 'exercise_plan':
                plan = get_object_or_404(ExercisePlan, pk=iid)
            elif itype == 'nutrition_plan':
                plan = get_object_or_404(NutritionPlan, pk=iid)
            if plan:
                sub, created = Subscription.objects.get_or_create(
                    user=user,
                    exercise_plan=plan if itype == 'exercise_plan' else None,
                    nutrition_plan=plan if itype == 'nutrition_plan' else None,
                    defaults={
                        'stripe_subscription_id': sess.subscription,
                        'stripe_customer_id': sess.customer,
                        'is_active': True,
                    },
                )
                if not created:
                    sub.stripe_subscription_id = sess.subscription
                    sub.stripe_customer_id = sess.customer
                    sub.is_active = True
                    sub.save()
            request.session['payment_status'] = 'success'
        else:
            request.session['payment_status'] = 'failure'
        return redirect('order_confirmation')
    if secret:
        pi_id = secret.split('_secret_')[0]
        try:
            pi = stripe.PaymentIntent.retrieve(pi_id)
        except stripe.error.StripeError as exc:
            messages.error(request, f'Error verifying payment: {exc}')
            return redirect('cart_detail')
        if pi.status == 'succeeded':
            cart = getattr(request.user, 'cart', None)
            if not cart or not cart.items.exists():
                messages.error(request, 'Cart is empty.')
                return redirect('home')
            order = Order.objects.create(
                user=request.user,
                total_amount=cart.get_total_cost(),
                stripe_payment_intent_id=pi.id,
            )
            for ci in cart.items.all():
                obj = ci.get_item_object()
                OrderItem.objects.create(
                    order=order,
                    item_type=('exercise_plan' if ci.exercise_plan else
                               'nutrition_plan' if ci.nutrition_plan else
                               'product'),
                    item_id=obj.id,
                    item_name=(
                        obj.title if hasattr(obj, 'title') else obj.name
                    ),
                    quantity=ci.quantity,
                    price=ci.price_at_addition,
                )
            cart.items.all().delete()
            cart.delete()
            request.session['payment_status'] = 'success'
        elif pi.status in ('processing', 'requires_action'):
            request.session['payment_status'] = 'pending'
        else:
            request.session['payment_status'] = 'failure'
        return redirect('order_confirmation')
    messages.error(request, 'No payment info found.')
    return redirect('home')


@login_required
def order_history(request):  # list past orders
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'registration/order_history.html',
                  {'orders': orders})
