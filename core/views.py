from rest_framework import viewsets, generics, status
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response

from core.models import Branch, Account
from core.permissions import IsAuthenticatedCustomer
from core.serializers import BranchSerializer, CustomerRegistrationSerializer, CustomerSerializer, AccountSerializer


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


class CustomerAccountViewSet(viewsets.ModelViewSet):
    queryset = Account.get_all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticatedCustomer]

    def create_account(self, request, *args, **kwargs):
        request.data['customer_id'] = request.user.customer.pk

        return super().create(request, *args, **kwargs)

    def close_account(self, request):
        account = getattr(request.user.customer, 'account', None)
        if not account:
            raise NotFound('You do not have any account to close!')
        branch = Branch.get_by_pk(request.data['branch_id'])

        if branch == account.branch:
            account.close()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        raise PermissionDenied('You can only close your account in the {} branch!'.format(account.branch))
