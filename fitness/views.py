import json

import mailchimp_marketing as mailchimp
import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from mailchimp_marketing.api_client import ApiClientError

from .forms import CustomUserCreationForm, NewsletterForm, ReviewForm
from .models import (Cart, CartItem, ExercisePlan, NutritionPlan, Order,
                     OrderItem, Product, Subscription, Review)


@login_required
def profile(request):  # show user profile
    active = request.user.subscriptions.filter(is_active=True).select_related(
        'exercise_plan', 'nutrition_plan'
    )
    return render(request, 'registration/profile.html', {'active': active})


def register(request):  # create new user
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created, please log in.')
            return redirect('login')
        for field, errors in form.errors.items():
            for err in errors:
                nice = field.replace('password1', 'password').replace(
                    'password2', 'password confirmation'
                )
                messages.error(request, f'Error in {nice}: {err}')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def home(request):  # landing page with featured items
    products = Product.objects.all().annotate(
        average_rating=Avg('reviews__rating'), review_count=Count('reviews')
    )[:3]
    ex_plans = ExercisePlan.objects.all().annotate(
        average_rating=Avg('reviews__rating'), review_count=Count('reviews')
    )[:3]
    nu_plans = NutritionPlan.objects.all().annotate(
        average_rating=Avg('reviews__rating'), review_count=Count('reviews')
    )[:3]
    ctx = {
        'featured_products': products,
        'featured_exercise_plans': ex_plans,
        'featured_nutrition_plans': nu_plans,
    }
    return render(request, 'public-pages/home.html', ctx)


def exercise_plan_list(request):  # list exercise plans
    plans = ExercisePlan.objects.all().annotate(
        average_rating=Avg('reviews__rating'), review_count=Count('reviews')
    )
    return render(request, 'public-pages/exercise_plan_list.html',
                  {'plans': plans})


def nutrition_plan_list(request):  # list nutrition plans
    plans = NutritionPlan.objects.all().annotate(
        average_rating=Avg('reviews__rating'), review_count=Count('reviews')
    )
    return render(request, 'public-pages/nutrition_plan_list.html',
                  {'plans': plans})


def product_list(request):  # list products
    products = Product.objects.all().annotate(
        average_rating=Avg('reviews__rating'), review_count=Count('reviews')
    )
    return render(request, 'public-pages/product_list.html',
                  {'products': products})


def exercise_plan_detail(request, pk):  # show exercise plan detail
    plan = get_object_or_404(
        ExercisePlan.objects.annotate(
            average_rating=Avg('reviews__rating'),
            review_count=Count('reviews'),
        ),
        pk=pk,
    )
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                rev = form.save(commit=False)
                rev.user = request.user
                rev.exercise_plan = plan
                rev.save()
                messages.success(request, 'Review submitted.')
                return redirect('exercise_plan_detail', pk=pk)
            messages.error(request, 'Log in to submit a review.')
    else:
        form = ReviewForm()
    return render(
        request,
        'public-pages/exercise_plan_detail.html',
        {'plan': plan, 'reviews': plan.reviews.all(), 'form': form},
    )


def nutrition_plan_detail(request, pk):  # show nutrition plan detail
    plan = get_object_or_404(
        NutritionPlan.objects.annotate(
            average_rating=Avg('reviews__rating'),
            review_count=Count('reviews'),
        ),
        pk=pk,
    )
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                rev = form.save(commit=False)
                rev.user = request.user
                rev.nutrition_plan = plan
                rev.save()
                messages.success(request, 'Review submitted.')
                return redirect('nutrition_plan_detail', pk=pk)
            messages.error(request, 'Log in to submit a review.')
    else:
        form = ReviewForm()
    return render(
        request,
        'public-pages/nutrition_plan_detail.html',
        {'plan': plan, 'reviews': plan.reviews.all(), 'form': form},
    )


def product_detail(request, pk):  # show product detail
    product = get_object_or_404(
        Product.objects.annotate(
            average_rating=Avg('reviews__rating'),
            review_count=Count('reviews'),
        ),
        pk=pk,
    )
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                rev = form.save(commit=False)
                rev.user = request.user
                rev.product = product
                rev.save()
                messages.success(request, 'Review submitted.')
                return redirect('product_detail', pk=pk)
            messages.error(request, 'Log in to submit a review.')
    else:
        form = ReviewForm()
    return render(
        request,
        'public-pages/product_detail.html',
        {'product': product, 'reviews': product.reviews.all(), 'form': form},
    )


@login_required
def edit_review(request, pk):
    """Allow users to edit their own review."""
    review = get_object_or_404(Review, pk=pk, user=request.user)
    form = ReviewForm(request.POST or None, instance=review)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Review updated successfully.')
        if review.product:
            return redirect('product_detail', pk=review.product.pk)
        elif review.nutrition_plan:
            return redirect(
                'nutrition_plan_detail', pk=review.nutrition_plan.pk)
        elif review.exercise_plan:
            return redirect(
                'exercise_plan_detail', pk=review.exercise_plan.pk)

    return render(
        request, 'public-pages/review_form.html',
        {'form': form, 'review': review})


@login_required
def delete_review(request, pk):
    """Allow users to delete their own review."""
    review = get_object_or_404(Review, pk=pk, user=request.user)
    if review.product:
        plan_id = review.product.pk
    elif review.nutrition_plan:
        plan_id = review.nutrition_plan.pk
    elif review.exercise_plan:
        plan_id = review.exercise_plan.pk

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully.')
        if review.product:
            return redirect('product_detail', pk=plan_id)
        elif review.nutrition_plan:
            return redirect('nutrition_plan_detail', pk=plan_id)
        elif review.exercise_plan:
            return redirect('exercise_plan_detail', pk=plan_id)

    return redirect('home')


@require_POST
@login_required
def add_to_cart(request, item_type, pk):  # add chosen item to cart
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


@login_required
@require_POST
def create_subscription_checkout(request, item_type, pk):  # start sub flow
    if item_type == 'exercise_plan':
        plan = get_object_or_404(ExercisePlan, pk=pk)
    elif item_type == 'nutrition_plan':
        plan = get_object_or_404(NutritionPlan, pk=pk)
    else:
        messages.error(request, 'Invalid subscription type.')
        return redirect('home')
    if not plan.stripe_price_id:
        messages.error(request, 'Price ID not configured.')
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    if has_active_subscription(request.user, item_type, pk):
        messages.warning(
            request,
            'You already have an active subscription for this plan.'
        )
        return redirect(request.META.get(
            'HTTP_REFERER', 'subscribed_dashboard')
        )

    try:
        cs = stripe.checkout.Session.create(
            customer_email=request.user.email,
            payment_method_types=['card'],
            line_items=[{'price': plan.stripe_price_id, 'quantity': 1}],
            mode='subscription',
            success_url=(
                request.build_absolute_uri(
                    '/payment-success/?session_id='
                ) + '{CHECKOUT_SESSION_ID}'
            ),
            cancel_url=request.build_absolute_uri('/checkout/?cancelled=true'),
            metadata={
                'user_id': request.user.id,
                'item_type': item_type,
                'item_id': plan.id,
            },
        )
    except stripe.error.StripeError as exc:
        messages.error(request, f'Error starting checkout: {exc}')
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    return redirect(cs.url, code=303)


'''
Helper function to check if a user has an active subscription.
'''


def has_active_subscription(user, plan_type=None, plan_id=None):
    if not user.is_authenticated:
        return False
    subs = user.subscriptions.filter(is_active=True)
    if plan_type == 'exercise_plan' and plan_id:
        return subs.filter(exercise_plan__id=plan_id).exists()
    if plan_type == 'nutrition_plan' and plan_id:
        return subs.filter(nutrition_plan__id=plan_id).exists()
    if plan_type is None:
        return subs.exists()
    return False


# function for successful subscription
@login_required
def subscription_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        messages.error(request, "No session ID provided.")
        return redirect('home')

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        customer_email = session.get('customer_email')

        messages.success(request, "Your subscription was successful! 🎉")
        # Optionally, activate subscription in DB
        # Example: Subscription.objects.create(user=request.user...)
    except Exception as e:
        messages.error(request, f"Error confirming subscription: {e}")
        return redirect('home')

    return redirect('subscribed_dashboard')


# function called when subscription is canceled
@login_required
def subscription_cancel(request):
    messages.warning(request, "Subscription checkout was cancelled.")
    return redirect('subscribed_dashboard')


# subscription dashboard
@login_required
def subscribed_dashboard(request):
    if not has_active_subscription(request.user):
        messages.warning(request, 'Active subscription required.')
        return redirect('home')

    from fitness.models import ExercisePlan, NutritionPlan  # safe import here

    active = Subscription.objects.filter(user=request.user, is_active=True)

    # Determine which type(s) of plan the user currently has
    active_exercise_ids = [
        sub.exercise_plan.id for sub in active if sub.exercise_plan
    ]
    active_nutrition_ids = [
        sub.nutrition_plan.id for sub in active if sub.nutrition_plan
    ]

    # Load available plans based on what they are subscribed to
    available_exercise_plans = ExercisePlan.objects.exclude(
        id__in=active_exercise_ids
    )
    available_nutrition_plans = NutritionPlan.objects.exclude(
        id__in=active_nutrition_ids
    )

    context = {
        "active_subscriptions": active,
        "available_exercise_plans": available_exercise_plans,
        "available_nutrition_plans": available_nutrition_plans,
    }

    return render(
        request,
        'registration/subscribed_dashboard.html',
        context,
    )


@login_required
def exercise_plan_content(request, pk):  # gated exercise content
    plan = get_object_or_404(ExercisePlan, pk=pk)
    if not has_active_subscription(request.user, 'exercise_plan', plan.id):
        messages.error(request, 'Subscription required.')
        return redirect('exercise_plan_detail', pk=pk)
    return render(request, 'registration/exercise_plan_content.html',
                  {'plan': plan})


@login_required
def nutrition_plan_content(request, pk):  # gated nutrition content
    plan = get_object_or_404(NutritionPlan, pk=pk)
    if not has_active_subscription(request.user, 'nutrition_plan', plan.id):
        messages.error(request, 'Subscription required.')
        return redirect('nutrition_plan_detail', pk=pk)
    return render(request, 'registration/nutrition_plan_content.html',
                  {'plan': plan})


def newsletter_signup(request):  # sign up to newsletter
    if request.method != 'POST':
        return redirect('home')
    form = NewsletterForm(request.POST)
    if not form.is_valid():
        messages.error(request, 'Enter a valid email.')
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    email = form.cleaned_data['email']
    try:
        client = mailchimp.Client()
        client.set_config({
            'api_key': settings.MAILCHIMP_API_KEY,
            'server': settings.MAILCHIMP_SERVER_PREFIX,
        })
        client.lists.add_list_member(
            settings.MAILCHIMP_AUDIENCE_ID,
            {'email_address': email, 'status': 'subscribed'},
        )
        messages.success(request, 'Subscribed to newsletter.')
    except ApiClientError as err:
        try:
            details = json.loads(err.text)
            if details.get('title') == 'Member Exists':
                messages.warning(request, 'Email already subscribed.')
            else:
                messages.error(
                    request,
                    f"Mailchimp error: {details.get('detail')}"
                )
        except json.JSONDecodeError:
            messages.error(request, 'Mailchimp unknown error.')
    except Exception as exc:
        messages.error(request, f'Error: {exc}')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def staff_dashboard(request):  # Renders the staff dashboard
    if not request.user.is_staff:
        messages.error(request, 'Staff only.')
        return redirect('home')
    users = User.objects.prefetch_related('subscriptions').order_by('username')
    data = []
    subs_cnt = staff_cnt = active_cnt = 0
    for u in users:
        paying = u.subscriptions.filter(is_active=True).exists()
        tags = []
        if paying:
            tags.append('subscriber')
            subs_cnt += 1
        if u.is_staff:
            tags.append('staff')
            staff_cnt += 1
        if u.is_active:
            active_cnt += 1
        data.append({'user': u, 'paying': paying,
                     'data_user_type': ' '.join(tags)})
    ctx = {
        'users_data': data,
        'subscribers_count': subs_cnt,
        'staff_count': staff_cnt,
        'active_users_count': active_cnt,
    }
    return render(request, 'registration/staff_dashboard.html', ctx)


def custom_404_view(request, exception):  # Handles 404 Not Found errors
    return render(request, "404.html", status=404)
