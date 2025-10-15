from django.shortcuts import render
from django.db.models import Avg, Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .forms import ReviewForm
from .models import Product, Review


# Create your views here.
def product_list(request):  # list products
    products = Product.objects.all().annotate(
        average_rating=Avg('reviews__rating'), review_count=Count('reviews')
    )
    return render(request, 'public-pages/product_list.html',
                  {'products': products})


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
            return redirect('nutrition_plan_detail',
                            pk=review.nutrition_plan.pk)
        elif review.exercise_plan: 
            return redirect('exercise_plan_detail', pk=review.exercise_plan.pk)

    return render(request, 'public-pages/review_form.html',
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
