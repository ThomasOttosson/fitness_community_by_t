from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap
from fitness.sitemaps import (
    StaticViewSitemap,
    ExercisePlanSitemap,
    NutritionPlanSitemap,
    ProductSitemap
)
from fitness.views import custom_404_view
from django.contrib.auth.views import LoginView
from fitness.forms import CustomAuthenticationForm

# SITEMAP CONFIGURATION
sitemaps = {
    'static': StaticViewSitemap,
    'exercise_plans': ExercisePlanSitemap,
    'nutrition_plans': NutritionPlanSitemap,
    'products': ProductSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fitness.urls')),
    path(
        'accounts/login/',
        LoginView.as_view(
            template_name='registration/login.html',
            authentication_form=CustomAuthenticationForm
        ),
        name='login'
    ),
    path('accounts/', include('django.contrib.auth.urls')),
    path(
        'robots.txt',
        serve,
        {'path': 'robots.txt', 'document_root': settings.STATICFILES_DIRS[0]}
    ),
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# handler404 = custom_404_view
handler404 = 'fitness.views.custom_404_view'
