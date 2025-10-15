import json

import mailchimp_marketing as mailchimp
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render
from mailchimp_marketing.api_client import ApiClientError

from .forms import CustomUserCreationForm, NewsletterForm
from .models import (ExercisePlan, NutritionPlan)
from products.models import Product
from products.forms import ReviewForm
from subscriptions.views import has_active_subscription


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
