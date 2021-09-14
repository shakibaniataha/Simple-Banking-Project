from django.urls import path
from core import views

urlpatterns = [
    path('branches/', views.BranchViewSet.as_view({
        'get': 'list',
    })),
    path('customer/register/', views.CustomerRegistrationView.as_view()),
    path('customer/accounts/', views.CustomerAccountViewSet.as_view({
        'post': 'create_account',
    })),
    path('customer/accounts/close/', views.CustomerAccountViewSet.as_view({
        'post': 'close_account',
    })),
    path('customer/accounts/transfer/', views.CustomerAccountViewSet.as_view({
        'post': 'transfer',
    })),
    path('customer/accounts/deposit/', views.CustomerAccountViewSet.as_view({
        'post': 'deposit',
    })),
    path('customer/accounts/withdraw/', views.CustomerAccountViewSet.as_view({
        'post': 'withdraw',
    })),
]
