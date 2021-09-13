from rest_framework import viewsets, generics
from rest_framework.response import Response

from core.models import Branch
from core.serializers import BranchSerializer, CustomerRegistrationSerializer, CustomerSerializer


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.get_all()
    serializer_class = BranchSerializer


class CustomerRegistrationView(generics.GenericAPIView):
    serializer_class = CustomerRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        return Response({
            "customer": CustomerSerializer(customer, context=self.get_serializer_context()).data,
            "message": "Customer was created successfully. Now perform login to get your token."
        })
