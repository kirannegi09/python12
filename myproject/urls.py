from django.contrib import admin
from django.urls import path, include  # Only import once

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),  # Now only prefix with 'api/'
]
