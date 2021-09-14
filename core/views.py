from rest_framework import viewsets, generics, status
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
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
        if not request.user.customer.has_active_account:
            raise NotFound('You do not have any active account to close!')
        branch = Branch.get_by_pk(request.data['branch_id'])
        account = request.user.customer.account

        if branch == account.branch:
            account.close()

            # TODO: create a transaction to return the account's balance to the customer

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        raise PermissionDenied('You can only close your account in the {} branch!'.format(account.branch))

    def transfer(self, request):
        amount = request.data['amount']
        customer = request.user.customer
        to_account = Account.get_by_pk(request.data['account_id'])
        if not to_account:
            raise ValidationError('Destination account not found')
        
        if not to_account.customer.can_deposit():
            raise PermissionDenied('Cannot deposit to the destination account')
        
        if not customer.can_withdraw(amount):
            raise PermissionDenied('Cannot withdraw from the source account')
        
        from_account = customer.account
        from_account.withdraw(amount)
        to_account.deposit(amount)
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    def deposit(self, request):
        amount = request.data['amount']
        account = Account.get_by_pk(request.data['account_id'])
        if not account.customer.can_deposit():
            raise PermissionDenied('Cannot deposit to this account')

        account.deposit(amount)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def withdraw(self, request):
        amount = request.data['amount']
        if not request.user.customer.can_withdraw(amount):
            raise PermissionDenied('You cannot withdraw!')
        
        request.user.customer.account.withdraw(amount)
        return Response(status=status.HTTP_204_NO_CONTENT)
