from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect
from fitness.models import ExercisePlan, NutritionPlan
from .models import Subscription
from django.contrib import messages
from django.urls import reverse
import stripe


# Create your views here.
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

    # Has subscribtion before
    if has_active_subscription(request.user, item_type, pk):
        messages.warning(
            request,
            'You already have an active subscription for this plan.'
            )
        return redirect(request.META.get(
            'HTTP_REFERER', 'subscribed_dashboard'
            ))

    try:
        cs = stripe.checkout.Session.create(
            customer_email=request.user.email,
            payment_method_types=['card'],
            line_items=[{'price': plan.stripe_price_id, 'quantity': 1}],
            mode='subscription',
            success_url=request.build_absolute_uri(
                '/checkout/payment-success/') +
            '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(
                reverse('subscription_cancel')
            ),
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


# update subscription plan
@login_required
@require_POST
def update_subscription(request, subscription_id):
    """
    Upgrade or downgrade an existing active subscription
    to a new Exercise or Nutrition plan.
    """
    from fitness.models import ExercisePlan, NutritionPlan
    import stripe

    new_plan_id = request.POST.get("new_plan_id")

    if not new_plan_id:
        messages.error(request, "Please select a new plan to switch to.")
        return redirect("subscribed_dashboard")

    # Fetch the user’s subscription
    subscription = get_object_or_404(
        Subscription,
        stripe_subscription_id=subscription_id,
        user=request.user
    )

    # Determine the plan type

    if subscription.exercise_plan:
        current_plan_type = "exercise"
    else:
        current_plan_type = "nutrition"

    # Get the new plan based on the current type
    if current_plan_type == "exercise":
        new_plan = get_object_or_404(ExercisePlan, id=new_plan_id)
    else:
        new_plan = get_object_or_404(NutritionPlan, id=new_plan_id)

    try:
        # Retrieve the active Stripe subscription
        stripe_sub = stripe.Subscription.retrieve(
                subscription.stripe_subscription_id
            )

        # Modify subscription in Stripe
        stripe.Subscription.modify(
            stripe_sub.id,
            cancel_at_period_end=False,
            proration_behavior="create_prorations",
            items=[{
                "id": stripe_sub["items"]["data"][0].id,
                "price": new_plan.stripe_price_id,
            }],
        )

        # Update in your local DB
        if current_plan_type == "exercise":
            subscription.exercise_plan = new_plan
            subscription.nutrition_plan = None
        else:
            subscription.nutrition_plan = new_plan
            subscription.exercise_plan = None

        subscription.save()

        messages.success(
            request,
            f"""✅ Your {current_plan_type} plan has
            been updated to '{new_plan.title}'."""
        )
        return redirect("subscribed_dashboard")

    except stripe.error.InvalidRequestError as e:
        messages.error(request, f"Stripe error: {e.user_message or str(e)}")
    except Exception as e:
        messages.error(request, f"Unexpected error: {str(e)}")

    return redirect("subscribed_dashboard")


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
        # session = stripe.checkout.Session.retrieve(session_id)
        # customer_email = session.get('customer_email')

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
