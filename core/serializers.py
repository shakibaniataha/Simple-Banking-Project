from rest_framework import serializers

from core.models import Branch, Customer


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = (
            'name',
        )


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            'name',
            'username',
            'password',
            'phone_number'
        )

    def create(self, validated_data):
        customer = Customer.objects.create(**validated_data)

        return customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            'id',
            'name',
            'username',
            'phone_number',
            'created_at'
        )
