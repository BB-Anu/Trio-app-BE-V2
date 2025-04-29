from django.shortcuts import render
from requests import Response
from user_management.scripts import simple_unique_id_generation
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import *
from rest_framework.views import APIView
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from os import error
from django.shortcuts import get_object_or_404, render
from requests import Response
from mainapp.api_call import call_post_method_for_without_token
from user_management.service import load_function_names_from_config
from mainapp.models import *
from mainapp.serializers import *
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view


# Create your views here.
class CompanyListCreateView(APIView):
    def get(self, request):
        records = Company.objects.all()
        serializer = CompanySerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = CompanySerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = FunctionSerializer(records, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class SelectCompanyListCreateView(APIView):
    def get(self, request,pk):
        records = Company.objects.get(pk=pk)
        serializer = CompanySerializer(records, many=True)
        return Response(serializer.data)

class GetCompanyListCreateView(APIView):
    def get(self, request,pk):
        records = Company.objects.get(Branch=pk)
        serializer = CompanySerializer(records, many=True)
        return Response(serializer.data)

class SelectBranchListCreateView(APIView):
    def get(self, request,pk):
        records = Branch.objects.filter(company=pk)
        print('===records==',records)
        serializer = BranchSerializer(records, many=True)
        return Response(serializer.data)

class BranchListCreateView(APIView):
    def get(self, request):
        records = Branch.objects.all()
        serializer = BranchSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        print('Incoming POST data:', request.data)
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            branch = serializer.save(
                created_by=request.user if request.user.is_authenticated else None,
                update_by=request.user if request.user.is_authenticated else None
            )
            return Response(BranchSerializer(branch).data, status=status.HTTP_201_CREATED)
        print('Serializer Errors:', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BranchRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Branch.objects.get(pk=pk)
        except Branch.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = BranchSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = BranchSerializer(records, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class FunctionListCreateView(APIView):
    def get(self, request):
        records = Function.objects.all()
        serializer = FunctionSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FunctionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FunctionRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Function.objects.get(pk=pk)
        except Function.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = FunctionSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = FunctionSerializer(records, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class CountyListCreateView(APIView):
    def get(self, request):
        records = County.objects.all()
        serializer = CountySerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CountySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CountyRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return County.objects.get(pk=pk)
        except County.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = CountySerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = CountySerializer(records, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class RoleListCreateView(APIView):
    def get(self, request):
        records = Role.objects.all()
        serializer = RoleSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('serializer',serializer.errors)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Role
from .serializers import RoleSerializer

class RoleRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return None

    def get(self, request, pk):
        role = self.get_object(pk)
        if not role:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(role)
        return Response(serializer.data)

    def put(self, request, pk):
        print('------request.data', request.data)
        role = self.get_object(pk)
        if not role:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        role = self.get_object(pk)
        if role:
            role.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class SubCountyListCreateView(APIView):
    def get(self, request):
        records = SubCounty.objects.all()
        serializer = SubCountySerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubCountySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubCountyRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return SubCounty.objects.get(pk=pk)
        except SubCounty.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = SubCountySerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = SubCountySerializer(records, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class WardListCreateView(APIView):
    def get(self, request):
        records = Ward.objects.all()
        serializer = WardSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WardRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Ward.objects.get(pk=pk)
        except Ward.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = WardSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = WardSerializer(records, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    

class UserListCreateView(APIView):
    # permission_classes = [IsAuthenticated] 
    def get(self, request):
        print('====',request.user)
        user=User.objects.get(email=request.user)
        branch_id=user.branch.pk
        records = User.objects.filter(branch=branch_id,is_superuser=False)
        print('---records---',records)
        serializer = UserSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            user.password = make_password(request.data.get("password")) 
            user.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateCreateView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = UserSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request):
        try:
            print('===requ',request.data)
            Branch=request.data
            print('---', request.user)
            user = User.objects.get(pk=request.user.id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        print('----', user)
        user.branch_id = Branch
        user.save()
        
        serializer = UserSerializer(user)
        return Response(serializer.data)


    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)



class UserRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = UserSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = UserSerializer(records, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def get_logged_in_user(request):
    print('data',request.data)
    print('data',request)
    user = request.user
    return Response({
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    })

class FunctionSetupAPI(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            function_names = load_function_names_from_config()
            print("Loaded function names:", function_names)  # Debugging

            existing_functions = set(Function.objects.values_list('function_name', flat=True))
            print("Existing functions", existing_functions)  # Debugging

            new_functions = []
            created_count = 0

            for function_name in function_names:
                if function_name not in existing_functions:
                    print(f"Creating function: {function_name}")  # Debugging
                    function = Function.objects.create(function_name=function_name)
                    function.function_id = simple_unique_id_generation("FUN", function.id)
                    function.save()
                    new_functions.append(function.function_name)
                    created_count += 1

            # Fetch all functions from the database
            functions_list = [
            {'id': fid, 'function_name': fname} 
            for fid, fname in Function.objects.values_list('id', 'function_name')
            ]
            return Response({
                'status': 'success',
                'created': created_count,
                'existing': len(function_names) - created_count,
                'functions': functions_list  # Return all function names
            }, status=status.HTTP_201_CREATED if created_count > 0 else status.HTTP_200_OK)

        except Exception as e:
            print("Error:", str(e))  # Debugging
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
class FunctionAllAPI(APIView):
    """
    API to fetch all functions.
    """
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            permission_records = Function.objects.all()
            print('permission_records',permission_records)
            serializers = FunctionSerializer(permission_records, many=True)
            print('serializers',serializers.data)
            return Response({'status': 'success', 'data': serializers.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetUserPermissionAPI(APIView):
    """
    API to get permissions assigned to a specific role.
    """

    # permission_classes = [IsAuthenticated]

    def get(self, request, role_id):
        try:
            role_obj = get_object_or_404(Role, pk=role_id)
            print("Role found:", role_obj)  # Debugging

            permission_records = role_obj.permissions.all()
            print("Permissions:", permission_records)  # Debugging

            serializers = FunctionSerializer(permission_records, many=True)
            print("Serialized Data:", serializers.data)  # Debugging

            return Response({'success': True, 'data': serializers.data}, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error:", str(e))  # Debugging
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetPermissionAPI(APIView):
    """
    API to get permissions assigned to a specific role.
    """

    # permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user_obj = get_object_or_404(User, pk=user_id)
            print("Role found:", user_obj)  # Debugging

            permission_records = user_obj.roles.permissions.all()
            print("Permissions:", permission_records)  # Debugging

            serializers = FunctionSerializer(permission_records, many=True)
            print("Serialized Data:", serializers.data)  # Debugging

            return Response({'success': True, 'data': serializers.data}, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error:", str(e))  # Debugging
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetRolePermissionAPI(APIView):
    """
    API to get permissions assigned to a specific role.
    """

    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user_obj = get_object_or_404(Role, pk=pk)
            print("Role found:", user_obj)  # Debugging

            permission_records = user_obj.permissions.all()
            print("Permissions:", permission_records)  # Debugging

            serializers = FunctionSerializer(permission_records, many=True)
            print("Serialized Data:", serializers.data)  # Debugging

            return Response({'success': True, 'data': serializers.data}, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error:", str(e))  # Debugging
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    print('---',username,password)
    user = authenticate(email=username, password=password)
    print('user',user)
    if user is not None:
        print('===',user)
        # Generate tokens using SimpleJWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        serializers=UserSerializer(user).data
        # Include user details along with the tokens

        if user.is_superuser == True:
            all_data=Function.objects.all()
            data=PermissionSerializer(all_data,many=True).data

        else:
            if user.roles is not None:
                data_get=Role.objects.get(id=user.roles.id)
                permissions=data_get.permissions.all()
                data=PermissionSerializer(permissions,many=True).data
            else:
                data=[]
        user_data = {
            'user_data': serializers,
            'access': access_token,
            'refresh_token': str(refresh),
            'permission':data
        }
        return Response(user_data)
    else:
        return Response({'error': 'Invalid credentials'},status=400)
