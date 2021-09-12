from rest_framework import viewsets, permissions

from core.models import Branch
from core.serializers import BranchSerializer


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.get_all()
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAuthenticated]
