from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import SignupView, LoginView, FaqView, GetFaqView, FaqDetailView, FaqDeleteView, ImagesView, StateView, GetStateView, EditStateView, DeleteStateView, AddFooterView 

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('get-faq/', GetFaqView.as_view(), name='get-faq'),
    path('faq/<int:pk>/', FaqDetailView.as_view(), name='faq-detail'),
    path('delete-faq/<int:pk>/', FaqDeleteView.as_view(), name='delete-faq'),
    path('images/', ImagesView.as_view(), name='images'),

    path('add-state/', StateView.as_view(), name='state'),
    path('get-state/', GetStateView.as_view(), name='get-state'),
    path('edit-state/<int:pk>/', EditStateView.as_view(), name='edit-state'),
    path('delete-state/<int:pk>/', DeleteStateView.as_view(), name='delete-view'),

    path('add-footer', AddFooterView.as_view(), name='add-footer'),
]

# Add static route for media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
