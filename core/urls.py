from django.urls import path
from core import views

urlpatterns = [
    path('branch/', views.BranchViewSet.as_view({
        'get': 'list',
    })),
    path('customer/register/', views.CustomerRegistrationView.as_view()),
]
