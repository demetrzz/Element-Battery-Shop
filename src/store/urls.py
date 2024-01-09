from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shopping.urls')),
    path('', include('payment_processing.urls')),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)),] + urlpatterns
