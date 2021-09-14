from rest_framework import serializers

from core.models import Branch, Customer, BaseUserModel, Account, Clerk


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUserModel
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'created_at',
        )


class ClerkSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Clerk
        fields = (
            'user',
        )


class BranchSerializer(serializers.ModelSerializer):
    clerk = ClerkSerializer(read_only=True)

    class Meta:
        model = Branch
        fields = (
            'name',
            'clerk',
        )


class CustomerRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=255)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        password = validated_data.pop('password')
        user_data = {'username': validated_data.pop('username'), 'password': password,
                     'first_name': validated_data.pop('first_name', None),
                     'last_name': validated_data.pop('last_name', None)}

        user = BaseUserModel.objects.create(**user_data)
        user.set_password(password)
        user.save()
        validated_data['user'] = user
        customer = Customer.objects.create(**validated_data)

        return customer


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = (
            'user',
            'phone_number',
        )


class AccountSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.IntegerField(write_only=True)
    branch = BranchSerializer(read_only=True)
    branch_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Account
        fields = (
            'id',
            'customer',
            'customer_id',
            'branch',
            'branch_id',
            'is_active',
            'balance',
            'created_at',
        )
