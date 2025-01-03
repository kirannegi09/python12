from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import SignupView, LoginView, FaqView, GetFaqView, FaqDetailView, FaqDeleteView, ImagesView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('get-faq/', GetFaqView.as_view(), name='get-faq'),
    path('faq/<int:pk>/', FaqDetailView.as_view(), name='faq-detail'),
    path('delete-faq/<int:pk>/', FaqDeleteView.as_view(), name='delete-faq'),
    path('images/', ImagesView.as_view(), name='images'),
]

# Serve media files with the '/api/' prefix during development
if settings.DEBUG:
    urlpatterns += static('/api/media/', document_root=settings.MEDIA_ROOT)