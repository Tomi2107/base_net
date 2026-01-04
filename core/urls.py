from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView, LandingPageView, reels_view, store_view, groups_view, AccountSettingsView





urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    path('users/', include('accounts.urls', namespace='users')),

    path('social/', include('social.urls', namespace='social')),


    path('dashboard/', HomeView.as_view(), name="home"),
    path('', LandingPageView.as_view(), name='landing'),  # Home externo público
    path("lost-found/", include("lost_found.urls", namespace="lost_found")),
    path("parroquiales/", include("parroquiales.urls", namespace="parroquiales")),
    path('settings/', AccountSettingsView.as_view(), name='account_settings'),
    
    
    path("reels/", include("reels.urls", namespace="reels")),
    
    
    path("store/", include("store.urls", namespace="store")),


    path("groups/", include("groups.urls", namespace="groups")),
    
    path('pets/', include('pets.urls')),  # 👈 ESTO
    
    path("foster/", include("foster.urls", namespace="foster" )),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)