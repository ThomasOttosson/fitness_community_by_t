mport os

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
                     OrderItem, Product, Subscription)

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
