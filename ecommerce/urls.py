from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls', namespace='shop')),  # Include the app's URLs
    path('accounts/', include('django.contrib.auth.urls')),  # Includes logout functionality
    path('', include('shop.urls', namespace='shop')), 
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
