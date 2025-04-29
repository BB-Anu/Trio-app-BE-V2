from rest_framework import serializers
from .models import *

class FunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Function
        fields = "__all__"

class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.roles and instance.roles.name:
            rep["roles"] = {
                'id': str(instance.roles.id),
                'name': instance.roles.name
            }
        else:
            rep["roles"] = None
        return rep

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class SubCountySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCounty
        fields = "__all__"

class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = "__all__"

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

class BranchSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    class Meta:
        model = Branch
        fields = "__all__"
        read_only_fields = ("created_by", "update_by", "created_at", "update_at")

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Function
        fields = ["function_name"]