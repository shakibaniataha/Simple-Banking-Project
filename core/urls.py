from django.urls import path, include
from core import views

urlpatterns = [
    path('branch/', views.BranchViewSet.as_view({
        'get': 'list',
    }))
]
