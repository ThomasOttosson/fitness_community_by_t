from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap
# Sitemaps for SEO
from fitness.sitemaps import (
    StaticViewSitemap,
    ExercisePlanSitemap,
    NutritionPlanSitemap,
    ProductSitemap
)
from django.contrib.auth.views import LoginView
# Custom login form
from fitness.forms import CustomAuthenticationForm
import checkout 

# SITEMAP CONFIGURATION
sitemaps = {
    'static': StaticViewSitemap,
    'exercise_plans': ExercisePlanSitemap,
    'nutrition_plans': NutritionPlanSitemap,
    'products': ProductSitemap,
}

# URL routing for the project
urlpatterns = [
    # Django admin site
    path('admin/', admin.site.urls),
    # Fitness app URLs
    path('', include('fitness.urls')),
    path('products/', include('products.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('checkout/', include('checkout.urls')),
    path('payment-success/', checkout.views.payment_success, name='payment_success'),

    # Custom login view
    path(
        'accounts/login/',
        LoginView.as_view(
            template_name='registration/login.html',
            authentication_form=CustomAuthenticationForm
        ),
        name='login'
    ),
    # Built-in auth URLs
    path('accounts/', include('django.contrib.auth.urls')),
    # robots.txt for crawlers
    path(
        'robots.txt',
        serve,
        {'path': 'robots.txt', 'document_root': settings.STATICFILES_DIRS[0]}
    ),
    # sitemap.xml for search engines
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
]

# Serve static and media files in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# Custom 404 error handler
handler404 = 'fitness.views.custom_404_view'
