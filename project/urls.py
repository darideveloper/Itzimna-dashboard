from django.urls import path, include
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers

from core.views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    ValidateRefreshView,
)
from properties import views as properties_views
from leads import views as leads_views
from blog import views as blog_views
from content import views as content_views


# Setup drf router
router = routers.DefaultRouter()

# Properties endpoints
router.register(
    r'properties',
    properties_views.PropertyViewSet,
    basename='properties'
)
router.register(
    r'locations',
    properties_views.LocationViewSet,
    basename='locations'
)
router.register(
    r'companies',
    properties_views.CompanyViewSet,
    basename='companies'
)

# Leads endpoints
router.register(
    r'leads',
    leads_views.LeadView,
    basename='leads'
)

# Blog endpoints
router.register(
    r'posts',
    blog_views.PostViewSet,
    basename='posts'
)

# Content endpoints
router.register(
    r'best-developments-images',
    content_views.BestDevelopmentsImageViewSet,
    basename='best-developments-images'
)
router.register(
    r'search',
    content_views.SearchViewSet,
    basename='search'
)

urlpatterns = [
    # Redirects
    path(
        '',
        RedirectView.as_view(url='/admin/'),
        name='home-redirect-admin'
    ),
    path(
        'accounts/login/',
        RedirectView.as_view(url='/admin/'),
        name='login-redirect-admin'
    ),
    
    # Apps
    path('admin/', admin.site.urls),
    
    # drf
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/validate/', ValidateRefreshView.as_view(), name='token_validate'),
    path('api/', include(router.urls)),
]

if not settings.STORAGE_AWS:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)