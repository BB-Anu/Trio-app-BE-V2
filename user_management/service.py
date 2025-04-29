import json
from django.core.exceptions import ValidationError
from django.apps import apps
from user_management.scripts import simple_unique_id_generation
from .models import *
from .serializers import *
from .middleware import get_current_request
from django.contrib.auth.hashers import make_password
import os
import random
from django.contrib.auth.hashers import check_password
    
def get_user(id=None):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        branch_id=request.user.branch

        if id is not None:
            record=User.objects.get(pk=id,branch=branch_id)
            serializers=UserSerializer(record)
            return success(serializers.data)
        else:
            instance = User.objects.filter(is_active=True,is_superuser=False,branch=branch_id)
            serializers=UserSerializer(instance,many=True)
            return success(serializers.data)
    
    except User.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")
    

def user_registration(first_name, last_name,address, email, phone_number, password,roles,maker,checker,is_admin,store_name,dob=None,gender=None,profile_image=None,):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        branch_id=request.user.branch
        instance = User.objects.create(
            # company=company,
            branch=branch_id,
            first_name=first_name,
            last_name=last_name,
            address=address,
            is_admin=is_admin,
            dob=dob,
            gender=gender,
            profile_image=profile_image,
            email=email,
            phone_number=phone_number,
            password=make_password(password),
            roles_id=roles,
            maker=maker,
            checker=checker
        )
        instance.store_name.set(store_name)
        instance.save()
        return success(f'Successfully created {instance} ')
    
    except User.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")
    

def user_edit(id ,first_name, last_name,address, email, phone_number, password,roles,maker,checker,is_admin,store_name,dob=None,gender=None,profile_image=None,):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        branch_id=request.user.branch
    
        instance = User.objects.get(pk=id)
        instance.first_name=first_name
        instance.last_name=last_name
        instance.address=address
        instance.is_admin=is_admin
        # instance.company=company
        instance.branch=branch_id
        instance.dob=dob
        instance.gender=gender
        instance.profile_image=profile_image
        instance.email=email
        instance.phone_number=phone_number
        instance.password=make_password(password)
        instance.roles_id=roles
        instance.maker=maker
        instance.checker=checker
        instance.store_name.set(store_name)
        instance.save()
        return success(f'Successfully Updated {instance} ')
    
    except User.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")
    
    
def user_delete(id):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        branch_id=request.user.branch

        instance = User.objects.get(pk=id,branch=branch_id)
        instance.is_active=False
        instance.save()
           
        return success(f'Successfully deleted {instance} ')
    
    except User.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")


def get_user_record():
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        branch_id=request.user.branch
        
        user_record = User.objects.filter(~Q(pk=request.user.pk),branch=branch_id)
        serializers=UserSerializer(user_record,many=True).data
        return success(serializers)

    except Exception as e:
        # Return an error response with the exception message
        return error(f"An error occurred: {e}")


def role_list(id=None):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        branch_id=request.user.branch
        
        if id is not None:
            record=Role.objects.get(pk=id,branch=branch_id)
            serializers=RoleSerializer(record).data
            return success(serializers)
        else:
            record=Role.objects.filter(branch=branch_id)
            serializers=RoleSerializer(record,many=True).data
            return success(serializers)
    
    except Role.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")

def role_create(name, description):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        branch_id=request.user.branch

        instance = Role.objects.create(
            branch=branch_id,
            name=name,
            description=description,
            created_by=request.user
        )
        return success(f'Successfully created {instance} ')
    
    except Role.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")
    

def role_edit(id,name, description):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        branch_id=request.user.branch

        instance = Role.objects.get(pk=id,branch=branch_id)
        instance.branch=branch_id
        instance.name=name
        instance.description=description
        instance.update_by=request.user
        instance.save()
        return success(f'Successfully Updated {instance} ')
    
    except Role.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")
    

def role_delete(id):

    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return os.error('Login required')
        branch_id=request.user.branch

        instance = Role.objects.get(pk=id,branch=branch_id)
        instance.delete()           
        return success(f'Successfully deleted {instance} ')
    
    except Role.DoesNotExist:
        return error('Instance does not exist')
    except Exception as e:
        return error(f"An error occurred: {e}")
    

def get_user_permission(id):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        branch_id=request.user.branch
        role_obj = Role.objects.get(pk=id,branch=branch_id)
        permission_records = role_obj.permissions.all()
        serializers=FunctionSerializer(permission_records,many=True).data
        return success(serializers)

    except Exception as e:
        return error(f"An error occurred: {e}")


def function_all():
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        permission_records=Function.objects.all()
        serializers=FunctionSerializer(permission_records,many=True).data
        return success(serializers)

    except Exception as e:
        return error(f"An error occurred: {e}")


def update_user_permission(id,permission):
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        branch_id=request.user.branch
        
        role_obj = Role.objects.get(pk=id,branch=branch_id)
        role_obj.permissions.set(permission)
        role_obj.save()
        return success('success')

    except Exception as e:
        return error(f"An error occurred: {e}")


def logout():
    request = get_current_request()
    if not request.user.is_authenticated:
        return error('Login required')
    return success('logout successfully')


# Load the function names from the configuration file
def load_function_names_from_config(config_path='config/function_config.json'):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        return config.get('functions', [])

# Example usage in a view:
def function_setup():
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return os.error('Login required')
        branch_id=request.user.branch

        user = request.user  # Use the currently logged-in user
        function_names = load_function_names_from_config()  # Load from the configuration file
        
        records_list = []
       
        for function_name in function_names:
            # Check if the function already exists
            if not Function.objects.filter(function_name=function_name).exists():
                # Create a new function
                function = Function.objects.create(
                    branch=branch_id,
                    function_name=function_name,
                    description=None,  # You can modify this to add descriptions if needed
                    created_by=user
                )
                # Assign a unique ID to the function
                function.function_id = simple_unique_id_generation("FUN", function.id)
                function.save()  # Save only if it's a new record
                records_list.append(function.function_name)
            else:
                # Log if the function already exists
                print(f"Function '{function_name}' already exists.")

    except Exception as e:
        return error(f"An error occurred: {e}")
    
#=====================Multi Tenent MS=======================

def user_profile_get_all():
    try:
        request = get_current_request()
        if not request.user.is_authenticated:
            return error('Login required')
        permission_records=Function.objects.all()
        serializers=FunctionSerializer(permission_records,many=True).data
        return success(serializers)

    except Exception as e:
        return error(f"An error occurred: {e}")
