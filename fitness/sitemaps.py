from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import ExercisePlan, NutritionPlan, Product


# Sitemap for static pages like home and listing pages
class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return [
            'home',
            'exercise_plan_list',
            'nutrition_plan_list',
            'product_list'
        ]

    def location(self, item):
        return reverse(item)


# Sitemap for individual exercise plan detail pages
class ExercisePlanSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return ExercisePlan.objects.all()

    def lastmod(self, obj):
        return None

    def location(self, obj):
        return reverse('exercise_plan_detail', args=[obj.pk])


# Sitemap for individual nutrition plan detail pages
class NutritionPlanSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return NutritionPlan.objects.all()

    def lastmod(self, obj):
        return None

    def location(self, obj):
        return reverse('nutrition_plan_detail', args=[obj.pk])


# Sitemap for individual product detail pages
class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return None

    def location(self, obj):
        return reverse('product_detail', args=[obj.pk])
