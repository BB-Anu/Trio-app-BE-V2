from .models import *
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.db.models import Q
from django.forms.models import model_to_dict
import random
from itertools import chain
import string
import os
from django.db import models

#===Error Log function====

def error_log_v1(message):
    try:
        # Resolve base directory relative to the script's location
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(base_dir, "logs")
        
        # Ensure the logs directory exists
        os.makedirs(log_path, exist_ok=True)
        
        # Combine base log path with the log file name
        directory = os.path.join(log_path, 'log.txt')
        # print('error directory',directory)
        # Write the log message
        with open(directory, 'a+') as screen_file:
            screen_file.writelines(f'{message} - {datetime.datetime.now()}\n')
    except Exception as error:
        print('log_error:', error)

def id_generation(prefix=None):
    # print('prefix ', prefix)
    if prefix is not None:
        return str(str(prefix) + '-' + str(random.randint(1111, 9999)))
    else:
        return str('NA' + '-' + str(random.randint(1111, 9999)))

def simple_unique_id_generation(pre,obj):
    # Calculating the total number of* records and incrementing by 1
    if obj:
        tot_rec_count=obj + 1
    else:
        tot_rec_count=1
     # Creating a unique ID b   ased on the total record count and the provided prefix
    if len(str(tot_rec_count)) == 1:
        id=pre+'000'+str(tot_rec_count)
    elif  len(str(tot_rec_count)) == 2:
        id=pre+'00'+str(tot_rec_count)
    else: 
        id=pre+str(tot_rec_count)
    return id


counter = 1

def new_simple_unique_id_generation(pre):
    global counter
    # Create a unique ID based on the counter and the provided prefix
    if len(str(counter)) == 1:
        unique_id = pre + '000' + str(counter)
    elif len(str(counter)) == 2:
        unique_id = pre + '00' + str(counter)
    elif len(str(counter)) == 3:
        unique_id = pre + '0' + str(counter)
    else:
        unique_id = pre + str(counter)
    
    # Increment the counter for the next unique ID
    counter += 1
    return unique_id

def generate_random_id(prefix, length=8):
    # Generate a random string of the specified length using letters and digits
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    # Combine the prefix and random string
    random_id = prefix + random_part
    return random_id


# def record_history(request, app_name, model_name, record_id):
#     """
#     Moves a specific record from the source model to the history model and deletes the original record.

#     Args:
#         app_name (str): The name of the app where the models exist.
#         model_name (str): The name of the model to move to history.
#         record_id (int): The primary key of the record to be moved.

#     Returns:
#         bool: True if the operation was successful, False otherwise.

#     Raises:
#         Exception: Any error encountered during the process is caught and logged.
#     """
#     try:
#         branch = request.user.branch

#         # Dynamically retrieve the models using Django's apps registry
#         source_model = apps.get_model(app_name, f'{model_name}Live')
#         history_model = apps.get_model(app_name, f'{model_name}History')

#         # Fetch the specific record by primary key
#         source_records = source_model.objects.filter(pk=record_id, branch=branch)

#         if source_records.exists():
#             for record in source_records:
#                 custom_id = generate_custom_record_id(record.pk)
#                 record_count = history_model.objects.filter(code=record.pk, branch=branch).count()

#                 # Determine the audit status based on the current state
#                 if record_count == 0:
#                     audit_status = 'create'
#                 else:
#                     audit_status = 'update'

#                 if record.is_deactivate:
#                     record_count -= 1
#                     audit_status = 'delete'

#                 fields_and_values = {}
#                 many_to_many_fields = {}  # To store ManyToManyField values (IDs)

#                 # Loop through the fields and handle ManyToMany fields and ForeignKey fields
#                 for field in record._meta.get_fields():
#                     if isinstance(field, models.ManyToManyField):
#                         # For ManyToMany fields, serialize the related object IDs
#                         related_objects = getattr(record, field.name).all()
#                         related_object_ids = [related_obj.pk for related_obj in related_objects]
#                         many_to_many_fields[field.name] = related_object_ids
#                     elif isinstance(field, models.ForeignKey):
#                         # For ForeignKey fields, store only the related object's ID
#                         related_object = getattr(record, field.name, None)
#                         if related_object:
#                             fields_and_values[f"{field.name}_id"] = related_object.pk
#                     else:
#                         fields_and_values[field.name] = getattr(record, field.name)
#                 print('==field_namevalues==',fields_and_values)
#                 # Create a new record in the history model, copying all fields except the primary key
#                 history_record = history_model.objects.create(
#                     history_custom_record_id=custom_id,
#                     history_version=record_count,
#                     **fields_and_values,
#                 )

#                 # Save the history record
#                 history_record.save()
#                 print('print===historu==',history_record)
#                 # Now, handle ManyToMany fields separately after saving the history record
#                 for field_name, related_ids in many_to_many_fields.items():
#                     field = history_model._meta.get_field(field_name)
#                     if isinstance(field, models.ManyToManyField):
#                         # Fetch related objects using their IDs
#                         related_objects = field.related_model.objects.filter(pk__in=related_ids)
#                         # Set the ManyToMany relationship using .set()
#                         getattr(history_record, field_name).set(related_objects)
#                         print('======field==name===field_name',field_name)
#                 # Audit the record movement
#                 model_audit(request, app_name, model_name, record_id, audit_status)

#             return True
#         else:
#             error_log_v1("record_history raised error: record not found")
#             return False
#     except Exception as error:
#         error_log_v1(f"record_history function raised an error: {error}")
#         return False


# def record_history(request, app_name, model_name, record_id):
#     """
#     Moves a specific record from the source model to the history model and deletes the original record.

#     Args:
#         app_name (str): The name of the app where the models exist.
#         model_name (str): The name of the model to move to history.
#         record_id (int): The primary key of the record to be moved.

#     Returns:
#         bool: True if the operation was successful, False otherwise.

#     Raises:
#         Exception: Any error encountered during the process is caught and logged.
#     """
#     try:
#         branch = request.user.branch

#         # Dynamically retrieve the models using Django's apps registry
#         source_model = apps.get_model(app_name, f'{model_name}Live')
#         history_model = apps.get_model(app_name, f'{model_name}History')

#         # Fetch the specific record by primary key
#         source_records = source_model.objects.filter(pk=record_id, branch=branch)

#         if source_records.exists():
#             for record in source_records:
#                 custom_id = generate_custom_record_id(record.pk)
#                 record_count = history_model.objects.filter(code=record.pk, branch=branch).count()

#                 # Determine the audit status based on the current state
#                 if record_count == 0:
#                     audit_status = 'create'
#                 else:
#                     audit_status = 'update'

#                 if record.is_deactivate:
#                     record_count -= 1
#                     audit_status = 'delete'

#                 fields_and_values = {}

#                 # Loop through the fields and handle ManyToMany fields
#                 for field in record._meta.fields:
#                     if isinstance(field, models.ManyToManyField):
#                         # For ManyToMany fields, serialize the related object IDs
#                         related_objects = getattr(record, field.name).all()
#                         related_object_ids = [related_obj.id for related_obj in related_objects]
#                         fields_and_values[field.name] = related_object_ids
#                     else:
#                         fields_and_values[field.name] = getattr(record, field.name)
#                 print('===field_values==',fields_and_values)
#                 # Create a new record in the history model, copying all fields except the primary key
#                 history_record = history_model.objects.create(
#                     history_custom_record_id=custom_id,
#                     history_version=record_count,
#                     **fields_and_values,
#                 )

#                 # Save the history record
#                 history_record.save()

#                 # Audit the record movement
#                 model_audit(request, app_name, model_name, record_id, audit_status)

#             return True
#         else:
#             error_log_v1("record_history raised error: record not found")
#             return False
#     except Exception as error:
#         error_log_v1(f"record_history function raised an error: {error}")
#         return False


def record_history(request,app_name,model_name, record_id):
    """
    Moves a specific record from the source model to the history model and deletes the original record.

    Args:
        source_model_name (str): The name of the model from which records are to be moved.
        history_model_name (str): The name of the model where the record should be archived.
        record_id (int): The primary key of the record to be moved.
        is_deleted (None):

    Returns:
        bool: True if the operation was successful, False otherwise.

    Raises:
        Exception: Any error encountered during the process is caught and logged.
    """
    try:

        branch=request.user.branch

        # Dynamically retrieve the models using Django's apps registry
        source_model = apps.get_model(app_name, f'{model_name}Live')
        history_model = apps.get_model(app_name, f'{model_name}History')

        # Fetch the specific record by primary key
        source_records = source_model.objects.filter(pk=record_id,branch=branch)

        if source_records.exists():
            for record in source_records:
                aa=record
                custom_id = generate_custom_record_id(record.pk)
                record_count = history_model.objects.filter(code=record.pk,branch=branch).count()
                if record_count==0:
                    audit_status = 'create'
                else:
                    audit_status='update'
                
                if aa.is_deactivate:
                    record_count -= 1
                    audit_status='delete'

                fields_and_values = {
                    field.name: getattr(record, field.name)
                    for field in record._meta.fields
                }
                # Create a new record in the history model, copying all fields except the primary key
                history_record = history_model.objects.create(
                    history_custom_record_id=custom_id,
                    history_version=record_count,
                    **fields_and_values,
                )
                history_record.save()
             
                model_audit(request,app_name,model_name,record_id,audit_status)
            return True
        else:
            error_log_v1("record_history raised error: record not found")
            # print('record_history raised error: record not found')
            return False
    except Exception as error:
        error_log_v1(f"record_history function raised an error: {error}")
        # print('record_history function raised an error:', error)
        return False



def move_record_temp_to_live(request,app_name,model_name, record_id, exclude_fields=['temp_status', 'temp_notes','temp_record_type']):
    
    # print('move record temp to live three',request,app_name,model_name,record_id)
    """
    Moves a specific record from a temporary model to a live model and deletes the temp record.

    Args:
        temp_model_name (str): The name of the temporary model from which records are to be moved.
        live_model_name (str): The name of the live model where the record should be moved.
        history_model_name (str): The name of the history model where the history should be recorded.
        record_id (int): The primary key of the record to be moved.
        exclude_fields (list): A list of field names to exclude from the copy operation.

    Returns:
        bool: True if the operation was successful, False otherwise.

    Raises:
        Exception: Any error encountered during the process is caught and logged.
    """
    try:
        # Dynamically retrieve the models using Django's apps registry
        temp_model = apps.get_model(app_name, f'{model_name}Temp')
        live_model = apps.get_model(app_name, f'{model_name}Live')


        # Retrieve the temp_record
        temp_record = temp_model.objects.get(pk=record_id)

        # Get regular fields and their values
        fields_and_values = {
            field.name: getattr(temp_record, field.name)
            for field in temp_record._meta.fields
            if field.name not in exclude_fields
        }

        many_to_many_values = {}
        for m2m_field in temp_record._meta.many_to_many:
            if m2m_field.name not in exclude_fields:
                # Get the related model
                related_manager = getattr(temp_record, m2m_field.name)
                related_model = related_manager.model

                # Determine the primary key field to use ('code' or fallback to the first available field)
                primary_key_field = (
                    'code' if 'code' in [field.name for field in related_model._meta.fields] else related_model._meta.pk.name
                )

                # Safely fetch values for the ManyToManyField
                many_to_many_values[m2m_field.name] = list(
                    related_manager.values_list(primary_key_field, flat=True)
                ) if related_manager.exists() else []

        # Find the live record
        obj_live = live_model.objects.filter(pk=record_id).first()
        if obj_live:
            # Update regular fields
            for field, value in fields_and_values.items():
                setattr(obj_live, field, value)
            obj_live.save()

            # Update ManyToManyField relationships
            for m2m_field, value in many_to_many_values.items():
                related_manager = getattr(obj_live, m2m_field)

                if value:  # Only update if the list is not empty
                    related_objects = (
                        related_manager.model.objects.filter(code__in=value)
                        if 'code' in [field.name for field in related_manager.model._meta.fields]
                        else related_manager.model.objects.filter(id__in=value)
                    )
                    related_manager.set(related_objects)  # Update relationships
                else:
                # If the list is empty, clear the relationships
                    related_manager.clear()

            # Record the history
            record_history(request, app_name, model_name, obj_live.pk)

            # Optionally delete the record from the temporary model after moving
            temp_record.delete()
            return True
        else:
            # Create a new record
            live_record = live_model.objects.create(**fields_and_values)

            # Set ManyToManyField relationships
            for m2m_field, value in many_to_many_values.items():
                related_manager = getattr(live_record, m2m_field)
               
                related_objects = (
                    related_manager.model.objects.filter(code__in=value)
                    if 'code' in [field.name for field in related_manager.model._meta.fields]
                    else related_manager.model.objects.filter(id__in=value)
                )
                related_manager.set(related_objects)

            # Record the history
            record_history(request, app_name, model_name, live_record.pk)

            # Optionally delete the record from the temporary model after moving
            temp_record.delete()
            return True

    except temp_model.DoesNotExist:
        error_log_v1("move_record_temp_to_live raised error: record not found")
        # print('move_record_temp_to_live raised error: record not found')
        return False
    except Exception as error:
        error_log_v1(f"move_record_temp_to_live move_record_123_temp_to_live function raised an error: {error}")
        # print('move_record_temp_to_live move_record_123_temp_to_live function raised an error:', error)
        return False



#This script is used for move multivalue data with many to many data

def move_record_temp_to_live_for_multivalue(request, app_name, main_model_name, record_id, sub_models_name, field_name, exclude_fields=['temp_status', 'temp_notes', 'temp_record_type']):
    """
    Moves a specific record from a temporary model to a live model and deletes the temp record.

    Args:
        app_name (str): The name of the app where the models reside.
        main_model_name (str): The name of the main model.
        record_id (int): The primary key of the record to be moved.
        sub_models_name (list): A list of sub-model names that have the same pattern (e.g., sub-models related to the main model).
        field_name (str): The field name used to relate sub-models to the main model.
        exclude_fields (list): A list of field names to exclude from the copy operation.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    try:
        branch_id=request.user.branch

        # Dynamically retrieve the models using Django's apps registry
        temp_model = apps.get_model(app_name, f'{main_model_name}Temp')
        live_model = apps.get_model(app_name, f'{main_model_name}Live')

        # Fetch the specific record by primary key from the temporary model
        temp_record = temp_model.objects.get(pk=record_id,branch=branch_id)
        fields_and_values = {}
        for field in temp_record._meta.fields:
            if field.name not in exclude_fields:
                fields_and_values[field.name] = getattr(temp_record, field.name)

        many_to_many_values = {}
        for m2m_field in temp_record._meta.many_to_many:
            if m2m_field.name not in exclude_fields:
                # Get the related model
                related_manager = getattr(temp_record, m2m_field.name)
                related_model = related_manager.model

                # Determine the primary key field to use ('code' or fallback to the first available field)
                primary_key_field = (
                    'code' if 'code' in [field.name for field in related_model._meta.fields] else related_model._meta.pk.name
                )

                # Safely fetch values for the ManyToManyField
                many_to_many_values[m2m_field.name] = list(
                    related_manager.values_list(primary_key_field, flat=True)
                ) if related_manager.exists() else []

        obj_live = live_model.objects.filter(pk=record_id,branch=branch_id).first()
        if obj_live:
            # Update the existing record
            for field, value in fields_and_values.items():
                setattr(obj_live, field, value)
            obj_live.save()

            # Update ManyToManyField relationships
            for m2m_field, value in many_to_many_values.items():
                related_manager = getattr(obj_live, m2m_field)
                if value:  # Only update if the list is not empty
                    related_objects = (
                        related_manager.model.objects.filter(code__in=value)
                        if 'code' in [field.name for field in related_manager.model._meta.fields]
                        else related_manager.model.objects.filter(id__in=value)
                    )
                    related_manager.set(related_objects)  # Update relationships
                else:
                    related_manager.clear()  # If the list is empty, clear the relationships

            # Record the history
            record_history(request, app_name, main_model_name, obj_live.pk)

            # Optionally delete the record from the temporary model after moving
            main_id = obj_live.pk
        else:
            live_record = live_model.objects.create(**fields_and_values)

            # Set ManyToManyField relationships
            for m2m_field, value in many_to_many_values.items():
                related_manager = getattr(live_record, m2m_field)
                related_objects = (
                    related_manager.model.objects.filter(code__in=value)
                    if 'code' in [field.name for field in related_manager.model._meta.fields]
                    else related_manager.model.objects.filter(id__in=value)
                )
                related_manager.set(related_objects)

            # Record the history
            record_history(request, app_name, main_model_name, live_record.pk)
            main_id = live_record.pk

        # Process sub-models
        for sub_module in sub_models_name:
            temp_model = apps.get_model(app_name, f'{sub_module}Temp')
            live_model = apps.get_model(app_name, f'{sub_module}Live')

            # Fetch the specific records by primary key from the temporary model
            filter_filter = {
                f'{field_name}_id': main_id
            }

            sub_temp_records = temp_model.objects.filter(**filter_filter)
            for sub_temp_record in sub_temp_records:
                sub_fields_and_values = {
                    field.name: getattr(sub_temp_record, field.name)
                    for field in sub_temp_record._meta.fields
                    if field.name not in exclude_fields
                }
                sub_fields_and_values[f'{field_name}_id'] = main_id
                del sub_fields_and_values[f"{field_name}"]

                sub_many_to_many_values = {}
                for m2m_field in sub_temp_record._meta.many_to_many:
                    if m2m_field.name not in exclude_fields:
                        related_manager = getattr(sub_temp_record, m2m_field.name)
                        related_model = related_manager.model

                        primary_key_field = (
                            'code' if 'code' in [field.name for field in related_model._meta.fields] else related_model._meta.pk.name
                        )

                        # Safely fetch values for the ManyToManyField
                        sub_many_to_many_values[m2m_field.name] = list(
                            related_manager.values_list(primary_key_field, flat=True)
                        ) if related_manager.exists() else []

                # Now, ensure `related_manager` is always properly defined
                sub_obj_live = live_model.objects.filter(**{f'{field_name}_id': main_id}).first()
                if sub_obj_live:
                    # Update the existing record
                    for field, value in sub_fields_and_values.items():
                        setattr(sub_obj_live, field, value)
                    sub_obj_live.save()

                    # Update ManyToManyField relationships
                    for m2m_field, value in sub_many_to_many_values.items():
                        related_manager = getattr(sub_obj_live, m2m_field)
                        if value:
                            related_objects = (
                                related_manager.model.objects.filter(code__in=value)
                                if 'code' in [field.name for field in related_manager.model._meta.fields]
                                else related_manager.model.objects.filter(id__in=value)
                            )
                            related_manager.set(related_objects)
                        else:
                            related_manager.clear()

                    # Record the history
                    record_history(request, app_name, sub_module, sub_obj_live.pk)

                    # Optionally delete the record from the temporary model after moving
                    sub_temp_record.delete()
                else:
                    live_record = live_model.objects.create(**sub_fields_and_values)

                    # Set ManyToManyField relationships
                    for m2m_field, value in sub_many_to_many_values.items():
                        related_manager = getattr(live_record, m2m_field)
                        related_objects = (
                            related_manager.model.objects.filter(code__in=value)
                            if 'code' in [field.name for field in related_manager.model._meta.fields]
                            else related_manager.model.objects.filter(id__in=value)
                        )
                        related_manager.set(related_objects)

                    # Record the history
                    record_history(request, app_name, sub_module, live_record.pk)

                    # Optionally delete the record from the temporary model after moving
                    sub_temp_record.delete()

        temp_record.delete()
        return True
    except temp_model.DoesNotExist:
        error_log_v1("move_record_temp_to_live raised error: record not found")
        # print('move_record_temp_to_live raised error: record not found')
        return False
    except Exception as error:
        error_log_v1(f"move_record_temp_to_live function raised an error: {error}")
        # print('move_record_temp_to_live function raised an error:', error)
        return False


def maker_checker_validation(request, model_name, pk):
    """
    Validates if a specific record from a temporary model can be moved to a live model based on maker-checker rules.

    Args:
        request: The HTTP request object containing the user information.
        model_name (str): The base name of the model (without 'Temp' or 'Audit' suffixes).
        pk (int): The primary key of the record in the temporary model to be validated.

    Returns:
        bool: True if the validation is successful and the checker is authorized, False otherwise.

    Raises:
        Exception: Catches and logs any error encountered during the process.
    """
    try:
        # Dynamically retrieve the models using Django's apps registry
        temp_model = apps.get_model('mainapp', f'{model_name}Temp')
        audit_model = apps.get_model('mainapp', f'{model_name}Audit')

        # Fetch the specific record by primary key from the temporary model
        temp_instance = temp_model.objects.filter(pk=pk)
        if not temp_instance.exists():
            # print('Data does not exist')
            return False

        temp_obj = temp_instance.last()

        # Fetch the corresponding audit record using a common attribute (e.g., code)
        audit_instance = audit_model.objects.filter(code=temp_obj.code)
        if not audit_instance.exists():
            # print('Audit data does not exist')
            return False

        # Retrieve the maker of the specific record
        maker = audit_instance.last().created_by

        # Check if the current user is an authorized checker for the maker
        checkers = MakerCheckerMapping.objects.filter(maker=maker, checker=request.user)
        if checkers.exists():
            return True
        else:
            error_log_v1("Checker does not exist for this user")
            # print("Checker does not exist for this user")
            return False

    except ObjectDoesNotExist as e:
        error_log_v1(f"ObjectDoesNotExist error: {e}")
        # print(f"ObjectDoesNotExist error: {e}")
        return False
    except Exception as error:
        error_log_v1(f"maker_checker_validation function raised an error: {error}")
        # print(f'maker_checker_validation function raised an error: {error}')
        return False


def checker_temp_records(request, model_name):
    """
    Validates if specific records from a temporary model can be moved to a live model based on maker-checker rules.

    Args:
        request: The HTTP request object containing the user information.
        model_name (str): The base name of the model (without 'Temp' or 'Audit' suffixes).

    Returns:
        bool: True if the validation is successful and the checker is authorized, False otherwise.

    Raises:
        Exception: Catches and logs any error encountered during the process.
    """
    try:
        # Dynamically retrieve the models using Django's apps registry
        temp_model = apps.get_model('mainapp', f'{model_name}Temp')
        audit_model = apps.get_model('mainapp', f'{model_name}Audit')

        # Fetch all codes from the temporary model
        temp_model_codes = temp_model.objects.values_list('code', flat=True)

        # Fetch audit records created by the current user with matching codes
        audit_instance_codes = audit_model.objects.filter(code__in=temp_model_codes,
                                                          created_by=request.user).values_list('code', flat=True)
  
        # Check if there are any matching records
        if temp_model.objects.filter(code__in=audit_instance_codes).exists():
            return True
        else:
            return False

    except ObjectDoesNotExist as e:
        error_log_v1(f"ObjectDoesNotExist error: {e}")
        # print(f"ObjectDoesNotExist error: {e}")
        return False
    except Exception as error:
        error_log_v1(f"checker_temp_records function raised an error: {error}")
        # print(f'checker_temp_records function raised an error: {error}')
        return False


def generate_custom_record_id(record_pk):
    # Get the current datetime
    now = datetime.datetime.now()

    # Convert to milliseconds since epoch
    current_time_millis = int(now.timestamp() * 1000)

    # Create the custom ID
    custom_record_id = f"{str(record_pk)}*{current_time_millis}"

    return custom_record_id


def self_authorization(request,app_name,model_name, record_id,type, exclude_fields=['temp_status', 'temp_notes','temp_record_type']):
    """
    Moves a specific record from a temporary model to a live model and deletes the temp record.

    Args:
        temp_model_name (str): The name of the temporary model from which records are to be moved.
        live_model_name (str): The name of the live model where the record should be moved.
        history_model_name (str): The name of the history model where the history should to recorded.
        record_id (int): The primary key of the record to be moved.

    Returns:
        bool: True if the operation was successful, False otherwise.

    Raises:
        Exception: Any error encountered during the process is caught and logged.
    """
    try:
        branch=request.user.branch
        model_reg = ModelRegistration.objects.filter(model_name=model_name,branch=branch).last()
        if model_reg:
            model=WorkflowMapping.objects.get(workflow_type=type,table_name=model_reg,branch=branch)
            if model.self_authorized:

                move_temp_live = move_record_temp_to_live(request,app_name,model_name,record_id,exclude_fields)
                #is_audit = model_audit(request,app_name,model_name,record_id,type)
                
                return move_temp_live
           
            return True
        else:
            error_log_v1("Model is not register")
            # print("Model is not register")
            error='Model is not register'
            return error
    except Exception as error:
        error_log_v1(f"move_record_temp_to_live in self authorization function raised an error: {error}")
        # print('move_record_temp_to_live in self authorization function raised an error:', error)
        return error

def self_authorization_for_multivalue(request,app_name,model_name, record_id,type, sub_models_name, field_name, exclude_fields=['temp_status', 'temp_notes','temp_record_type']):
    """
    Moves a specific record from a temporary model to a live model and deletes the temp record.

    Args:
        temp_model_name (str): The name of the temporary model from which records are to be moved.
        live_model_name (str): The name of the live model where the record should be moved.
        history_model_name (str): The name of the history model where the history should to recorded.
        record_id (int): The primary key of the record to be moved.

    Returns:
        bool: True if the operation was successful, False otherwise.

    Raises:
        Exception: Any error encountered during the process is caught and logged.
    """
    try:
        branch_id=request.user.branch
        model_reg = ModelRegistration.objects.filter(model_name=model_name,branch_id=branch_id).last()
        if model_reg:
            model=WorkflowMapping.objects.get(workflow_type=type,table_name=model_reg,branch_id=branch_id)
            if model.self_authorized:
                
                move_temp_live = move_record_temp_to_live_for_multivalue(request,app_name,model_name, record_id, sub_models_name, field_name, exclude_fields)
                is_audit = model_audit(request,app_name,model_name,record_id,type)
                return move_temp_live
           
            return True
        else:
            error_log_v1("Model is not register")
            # print("Model is not register")
            return False
    except Exception as error:
        error_log_v1(f"move_record_temp_to_live  function raised an error: {error}")
        # print('move_record_temp_to_live function raised an error:', error)
        return False


def delete_record(request,app_name, model_name, pk):
    branch=request.user.branch
    live_model = apps.get_model(app_name, f'{model_name}Live')
    live_record = live_model.objects.filter(pk=pk,branch=branch).last()
    if live_record:
        live_record.is_deactivate = True
        live_record.save()
        history = record_history(request,app_name,model_name, pk)
       
        if history:
            return True
        else:
            return False
    else:
        return False


def authorize_request(request,table_name_id, record_id, sender_user_id, approval_user_id,type=None,next_approval_user=None):
    try:
   
        obj = AuthorizeRequest(
            branch=request.user.branch,
            table_name_id=str(table_name_id),
            record_id=str(record_id),
            sender_user_id=str(sender_user_id),
            approval_user_id=str(approval_user_id),
            next_approval_user_id=next_approval_user if next_approval_user is None else str(next_approval_user),
            workflow_type=type if type is None else str(type)
        )
        obj.save()
        return True
    except Exception as error:
        error_log_v1(f"authorize_request  function raised an error: {error}")
        # print('authorize_request function raised error ', error)
        return error



# def get_record_for_authorize(user_id):
#     try:
#         obj = AuthorizeRequest.objects.filter(
#             Q(approval_user_id=user_id) & Q(is_authorized_return=False) & Q(is_authorized=False)
#         )
        
#         return obj
#     except Exception as error:
#         print('new_authorize_request function raised error ', error)
#         return False

def get_record_for_authorize(user_id,branch_id,model_name):
    try:
        obj = AuthorizeRequest.objects.filter(
            Q(approval_user_id=user_id) & Q(is_authorized_return=False) & Q(is_authorized=False) & Q(table_name__model_name__exact=model_name) & Q(branch_id=branch_id)
        )
        
        return obj
    except Exception as error:
        error_log_v1(f"get_record_for_authorize  function raised an error: {error}")
        # print('get_record_for_authorize function raised error ', error)
        return False

# def model_to_dict_many(instance, fields=None, exclude=None):
#     """
#     Return a dict containing the data in ``instance`` suitable for passing as
#     a Form's ``initial`` keyword argument.

#     ``fields`` is an optional list of field names. If provided, return only the named.

#     ``exclude`` is an optional list of field names. If provided, exclude the
#     named from the returned dict, even if they are listed in the ``fields`` argument.
#     """
#     opts = instance._meta
#     data = {}

#     # Iterate through all fields
#     for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
#         # Skip non-editable fields
#         if not getattr(f, "editable", False):
#             continue
        
#         # Skip fields not in the 'fields' list, if provided
#         if fields is not None and f.name not in fields:
#             continue
        
#         # Skip fields in the 'exclude' list, if provided
#         if exclude and f.name in exclude:
#             continue
        
#         # Check if the field is a ManyToMany field
#         if f.many_to_many:
#             # If it is, we want to serialize the related objects (e.g., the primary key or another field)
#             # Optionally, you can customize the serialized representation of the related model
#             related_data = [related_instance.pk for related_instance in getattr(instance, f.name).all()]
#             data[f.name] = related_data
#         else:
#             # For non ManyToMany fields, just get the value
#             data[f.name] = f.value_from_object(instance)
            
#     return data

from django.db.models import FileField, ImageField
from itertools import chain

def model_to_dict_many(instance, fields=None, exclude=None):
    """
    Return a dict containing the data in `instance` suitable for passing as
    a Form's `initial` keyword argument.

    `fields` is an optional list of field names. If provided, return only the named.

    `exclude` is an optional list of field names. If provided, exclude the
    named from the returned dict, even if they are listed in the `fields` argument.
    """
    opts = instance._meta
    data = {}

    # Iterate through all fields
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        # Skip non-editable fields
        if not getattr(f, "editable", False):
            continue
        
        # Skip fields not in the 'fields' list, if provided
        if fields is not None and f.name not in fields:
            continue
        
        # Skip fields in the 'exclude' list, if provided
        if exclude and f.name in exclude:
            continue
        
        # Check if the field is a ManyToMany field
        if f.many_to_many:
            # If it is, serialize the related objects (e.g., the primary key or another field)
            related_data = [related_instance.pk for related_instance in getattr(instance, f.name).all()]
            data[f.name] = related_data
        # Check if the field is a FileField or ImageField
        elif isinstance(f, (FileField, ImageField)):
            # For FileField/ImageField, use the URL if it exists, otherwise return None
            file_value = getattr(instance, f.name)
            data[f.name] = file_value.url if file_value else None
        else:
            # For non ManyToMany fields, just get the value
            data[f.name] = f.value_from_object(instance)
            
    return data

def convert_query_set_to_dict(obj):
    if obj:
        obj_dict = model_to_dict_many(obj)  # Convert the model instance to a dictionary
        obj_dict.pop('status', None)
        obj_dict.pop('notes', None)
        obj_dict.pop('is_deactivate', None)
    else:
        obj_dict = {}

    return obj_dict


def get_record_various_models_by_pk(app_name,model_name, record_id,type,output_as_dict=False,model_suffix="Temp"):
    try:
        if type == 'create' or type == 'update':
            temp_model_name = apps.get_model(app_name, f'{model_name}{model_suffix}')

            obj = temp_model_name.objects.get(pk=record_id)
        else:
            temp_model_name = apps.get_model(app_name, f'{model_name}Live')
            obj = temp_model_name.objects.get(pk=record_id)
  
        if output_as_dict:
            query_set_dict = convert_query_set_to_dict(obj)
            return query_set_dict
        else:
            return obj
    except Exception as error:
        error_log_v1(f"get_record_various_models_by_pk  function raised an error: {error}")
        # print('get_record_various_models_by_pk ', error)
        return False


def delegate_users(user_id, table_name, record_id,branch_id):
    try:
        obj = DelegateRecords(
            custom_record_id=generate_custom_record_id(record_id),
            table_name_id=table_name,
            delegate_to_id=user_id,
            branch_id=branch_id
        )
        obj.save()
        return True
    except Exception as error:
        error_log_v1(f"delegate_users  function raised an error: {error}")
        # print('Error ', error)
        return False

def is_have_permission(request,app_name,model_name,record_id):
    try:
        branch=request.user.branch
        delegate = DelegateRecords.objects.filter(custom_record_id__startswith=record_id,table_name__model_name=model_name,branch=branch)
        if delegate.exists():
            user = delegate.last().delegate_to
        else:
            audit_model_name = apps.get_model(app_name, f'{model_name}Audit')
            query_set_dict = audit_model_name.objects.filter(code=record_id,branch=branch)
            if query_set_dict.exists():
                user = query_set_dict.first().created_by
            else:
                return False
        if user == request.user:
            return True
        else:
            return False
    except Exception as error:
        error_log_v1(f"is_have_permission  function raised an error: {error}")
        # print('error ', error)
        return False
    
def get_temp_record(request,app_name,model_name):
    try:
        branch=request.user.branch
        temp_model_name = apps.get_model(app_name, f'{model_name}Temp')
        audit_model_name = apps.get_model(app_name, f'{model_name}Audit')
        temp_record = temp_model_name.objects.all()
        code_list=[]
        for data in temp_record:
            audit_records=audit_model_name.objects.filter(code=data.code,branch=branch,audit_status='in_temp').last()
            if audit_records:
                if audit_records.created_by == request.user:
                    code_list.append(data.code)
        temp_records = temp_model_name.objects.filter(code__in=code_list,branch=branch)
        return temp_records
    except Exception as error:
        error_log_v1(f"get_temp_record  function raised an error: {error}")
        # print(f'get_temp_record getting {error}')
        return False
    
# def model_audit(request, app_name, model_name, record_id, status='in_temp'):
#     try:
#         if status == 'in_temp':
#             record = apps.get_model(app_name, f'{model_name}Temp')
#         elif status in ['create', 'update', 'delete']:
#             record = apps.get_model(app_name, f'{model_name}Live')
#         else:
#             return False
        
#         # Get the audit model
#         audit_model_name = apps.get_model(app_name, f'{model_name}Audit')
        
#         # Get the object for the record ID
#         obj = record.objects.get(pk=record_id)
#         print('===obj===', obj)
        
#         # List of fields to exclude from audit (like 'temp_status' and others)
#         exclude_fields = ['temp_status', 'temp_notes', 'is_deactivate', 'temp_record_type']
        
#         # Dictionary to hold field names and their values
#         fields_and_values = {}
#         many_to_many_fields = {}  # To store many-to-many field values (IDs)
        
#         # Loop over all fields in the model to extract their values
#         for field in obj._meta.get_fields():
#             print('===field=name===', field)
        
#             if field.name not in exclude_fields:
#                 print('==field==', field)
                
#                 if isinstance(field, models.ManyToManyField):
#                     # Handle ManyToMany fields separately
#                     print('==field===', field.name)
#                     related_objects = getattr(obj, field.name).all()  # Get related objects of the ManyToMany field
#                     print('===related objects===', related_objects)
                    
#                     # Store the related object's IDs in the dictionary
#                     related_object_ids = [related_obj.pk for related_obj in related_objects]
#                     many_to_many_fields[field.name] = related_object_ids  # Store the IDs for later assignment
                    
#                 elif isinstance(field, models.ForeignKey):
#                     # For ForeignKey, store the ID of the related object
#                     related_object = getattr(obj, field.name, None)
#                     if related_object:
#                         fields_and_values[f"{field.name}_id"] = related_object.pk  # Store related object ID
                    
#                 else:
#                     # For other field types, store their values as usual
#                     fields_and_values[field.name] = getattr(obj, field.name)

#         # Create an audit record (without ManyToManyField assignments)
#         audit_record = audit_model_name.objects.create(
#             audit_custom_record_id=generate_custom_record_id(record_id),
#             created_by=request.user,
#             updated_by=request.user,
#             **fields_and_values,
#             audit_status=status,
#         )
#         print('===audit_record created===', audit_record)

#         # Now, handle ManyToMany fields separately after saving the audit record
#         for field_name, related_ids in many_to_many_fields.items():
#             field = audit_model_name._meta.get_field(field_name)
#             print(f"Handling ManyToMany field: {field_name}")
            
#             if isinstance(field, models.ManyToManyField):
#                 # Fetch related objects using their IDs
#                 related_objects = field.related_model.objects.filter(pk__in=related_ids)
#                 # Set the ManyToMany relationship using .set()
#                 getattr(audit_record, field_name).set(related_objects)

#         return True
#     except Exception as error:
#         error_log_v1(f"model_audit function raised an error: {error}")
#         print('===error==', error)
#         return error

# def model_audit(request, app_name, model_name, record_id, status='in_temp'):
#     try:
#         if status == 'in_temp':
#             record = apps.get_model(app_name, f'{model_name}Temp')
#         elif status == 'create' or status == 'update' or status == 'delete':
#             record = apps.get_model(app_name, f'{model_name}Live')
#         else:
#             return False
        
#         # Get the audit model
#         audit_model_name = apps.get_model(app_name, f'{model_name}Audit')
        
#         # Get the object for the record ID
#         obj = record.objects.get(pk=record_id)
#         print('===obj===', obj)
        
#         # List of fields to exclude from audit (like 'temp_status' and others)
#         exclude_fields = ['temp_status', 'temp_notes', 'is_deactivate', 'temp_record_type']
        
#         # Dictionary to hold field names and their values
#         fields_and_values = {}
#         fields_and_value = {}
        
#         # Loop over all fields in the model to extract their values
#         for field in obj._meta.get_fields():  # Use get_fields() instead of _meta.fields for related fields
#             print('===field=name===', field)
        
#             if field.name not in exclude_fields:
#                 print('==field==', field)
                
#                 if isinstance(field, models.ManyToManyField):
#                     # Handle ManyToMany fields separately
#                     print('==field===', field.name)
#                     related_objects = getattr(obj, field.name).all()  # This gets the related objects of the ManyToMany field
#                     print('===related objects===', related_objects)
                    
#                     # Store the related object's IDs in the dictionary
#                     related_object_ids = [related_obj.pk for related_obj in related_objects]
#                     fields_and_value[field.name] = related_object_ids  # Store the IDs in the dictionary
                    
#                 elif isinstance(field, models.ForeignKey):
#                     # If it's a ForeignKey, save the related object's ID
#                     related_object = getattr(obj, field.name, None)
#                     if related_object:
#                         fields_and_values[f"{field.name}_id"] = related_object.pk  # Save only the ID of the related object
#                         fields_and_value[f"{field.name}_id"] = related_object.pk  # Save only the ID of the related object
                
#                 else:
#                     # For other field types, just store their value as usual
#                     fields_and_values[field.name] = getattr(obj, field.name)
#                     fields_and_value[field.name] = getattr(obj, field.name)
                    

#                 print('===fields_and_values after processing===', fields_and_values)

#         # Create an audit record (without ManyToManyField assignments)
#         audit_record = audit_model_name.objects.create(
#             audit_custom_record_id=generate_custom_record_id(record_id),
#             created_by=request.user,
#             updated_by=request.user,
#             **fields_and_values,
#             audit_status=status,
#         )
#         print('===audit--record--',audit_record)
#         # After the audit record is created, handle ManyToMany fields using .set() method
#         for field_name, value in fields_and_value.items():
#             field = audit_model_name._meta.get_field(field_name)
#             print('==field=123=', field)
#             # Check if it's a ManyToManyField and use .set() method to assign related objects
#             if isinstance(field, models.ManyToManyField):
#                 # Fetch the related objects from their IDs
#                 related_objects = field.related_model.objects.filter(pk__in=value)
#                 # Now set the ManyToMany relationship using .set()
#                 getattr(audit_record, field_name).set(related_objects)  # Use .set() to assign related objects to the ManyToMany field

#         return True
#     except Exception as error:
#         error_log_v1(f"model_audit function raised an error: {error}")
#         print('===error==', error)
#         return error


# def model_audit(request, app_name, model_name, record_id, status='in_temp'):
#     try:
#         if status == 'in_temp':
#             record = apps.get_model(app_name, f'{model_name}Temp')
#         elif status == 'create' or status == 'update' or status == 'delete':
#             record = apps.get_model(app_name, f'{model_name}Live')
#         else:
#             return False
        
#         # Get the audit model
#         audit_model_name = apps.get_model(app_name, f'{model_name}Audit')
        
#         # Get the object for the record ID
#         obj = record.objects.get(pk=record_id)
#         print('===obj===', obj)
        
#         # List of fields to exclude from audit (like 'temp_status' and others)
#         exclude_fields = ['temp_status', 'temp_notes', 'is_deactivate', 'temp_record_type']
        
#         # Dictionary to hold field names and their values
#         fields_and_values = {}
        
#         # Loop over all fields in the model to extract their values
#         for field in obj._meta.get_fields():  # Use get_fields() instead of _meta.fields for related fields
#             print('===field=name===', field)
        
#             if field.name not in exclude_fields:
#                 print('==field==', field)
                
#                 if isinstance(field, models.ManyToManyField):
#                     # Handle ManyToMany fields separately
#                     print('==field===', field.name)
#                     related_objects = getattr(obj, field.name).all()  # This gets the related objects of the ManyToMany field
#                     print('===related objects===', related_objects)
                    
#                     # You can store the related object's IDs, or serialize them based on your need
#                     related_object_ids = [related_obj.pk for related_obj in related_objects]
#                     fields_and_values[field.name] = related_object_ids  # Store the IDs in the dictionary
                    
#                 elif isinstance(field, models.ForeignKey):
#                     # If it's a ForeignKey, save the related object's ID
#                     related_object = getattr(obj, field.name, None)
#                     if related_object:
#                         fields_and_values[f"{field.name}_id"] = related_object.pk  # Save only the ID of the related object
                
#                 else:
#                     # For other field types, just store their value as usual
#                     fields_and_values[field.name] = getattr(obj, field.name)
                    

#                 print('===fields_and_values after processing===', fields_and_values)

#         # Create an audit record
#         audit_record = audit_model_name.objects.create(
#             audit_custom_record_id=generate_custom_record_id(record_id),
#             created_by=request.user,
#             updated_by=request.user,
#             **fields_and_values,
#             audit_status=status,
#         )
        
#         # After creating the audit record, we need to handle ManyToMany fields
#         for field_name, value in fields_and_values.items():
#             field = audit_model_name._meta.get_field(field_name)
            
#             # Check if it's a ManyToManyField and use .set() method
#             if isinstance(field, models.ManyToManyField):
#                 # Fetch related objects and use .set() to assign them
#                 related_objects = field.related_model.objects.filter(pk__in=value)
#                 getattr(audit_record, field_name).set(related_objects)  # Use .set() to assign related objects to the ManyToMany field
        
#         return True
#     except Exception as error:
#         error_log_v1(f"model_audit function raised an error: {error}")
#         print('===error==', error)
#         return error

# def model_audit(request, app_name, model_name, record_id, status='in_temp'):
#     try:
#         if status == 'in_temp':
#             record = apps.get_model(app_name, f'{model_name}Temp')
#         elif status == 'create' or status == 'update' or status == 'delete':
#             record = apps.get_model(app_name, f'{model_name}Live')
#         else:
#             return False
        
#         # Get the audit model
#         audit_model_name = apps.get_model(app_name, f'{model_name}Audit')
        
#         # Get the object for the record ID
#         obj = record.objects.get(pk=record_id)
#         print('===obj===', obj)
        
#         # List of fields to exclude from audit (like 'temp_status' and others)
#         exclude_fields = ['temp_status', 'temp_notes', 'is_deactivate', 'temp_record_type']
        
#         # Dictionary to hold field names and their values
#         fields_and_values = {}
        
#         # Loop over all fields in the model to extract their values
#         for field in obj._meta.get_fields():  # Use get_fields() instead of _meta.fields for related fields
#             print('===field=name===', field)
        
#             if field.name not in exclude_fields:
#                 print('==field==', field)
                
#                 if isinstance(field, models.ManyToManyField):
#                     # Handle ManyToMany fields separately
#                     print('==field===', field.name)
#                     related_objects = getattr(obj, field.name).all()  # This gets the related objects of the ManyToMany field
#                     print('===related objects===', related_objects)
                    
#                     # Store the related object's IDs in the dictionary
#                     related_object_ids = [related_obj.pk for related_obj in related_objects]
#                     fields_and_values[field.name] = related_object_ids  # Store the IDs in the dictionary
                    
#                 elif isinstance(field, models.ForeignKey):
#                     # If it's a ForeignKey, save the related object's ID
#                     related_object = getattr(obj, field.name, None)
#                     if related_object:
#                         fields_and_values[f"{field.name}_id"] = related_object.pk  # Save only the ID of the related object
                
#                 else:
#                     # For other field types, just store their value as usual
#                     fields_and_values[field.name] = getattr(obj, field.name)
                    

#                 print('===fields_and_values after processing===', fields_and_values)

#         # Create an audit record
#         audit_record = audit_model_name.objects.create(
#             audit_custom_record_id=generate_custom_record_id(record_id),
#             created_by=request.user,
#             updated_by=request.user,
#             **fields_and_values,
#             audit_status=status,
#         )

#         # After creating the audit record, we need to handle ManyToMany fields
#         for field_name, value in fields_and_values.items():
#             field = audit_model_name._meta.get_field(field_name)
#             print('==field=123=',field)
#             # Check if it's a ManyToManyField and use .set() method
#             if isinstance(field, models.ManyToManyField):
#                 # Fetch related objects and use .set() to assign them
#                 related_objects = field.related_model.objects.filter(pk__in=value)
#                 getattr(audit_record, field_name).set(related_objects)  # Use .set() to assign related objects to the ManyToMany field

#         return True
#     except Exception as error:
#         error_log_v1(f"model_audit function raised an error: {error}")
#         print('===error==', error)
#         return error


# def model_audit(request, app_name, model_name, record_id, status='in_temp'):
#     try:
#         if status == 'in_temp':
#             record = apps.get_model(app_name, f'{model_name}Temp')
#         elif status == 'create' or status == 'update' or status == 'delete':
#             record = apps.get_model(app_name, f'{model_name}Live')
#         else:
#             return False
        
#         # Get the audit model
#         audit_model_name = apps.get_model(app_name, f'{model_name}Audit')
        
#         # Get the object for the record ID
#         obj = record.objects.get(pk=record_id)
#         print('===obj===',obj)
#         # List of fields to exclude from audit (like 'temp_status' and others)
#         exclude_fields = ['temp_status', 'temp_notes', 'is_deactivate', 'temp_record_type']
        
#         # Dictionary to hold field names and their values
#         fields_and_values = {}
        
#         # Loop over all fields in the model to extract their values
#         for field in obj._meta.fields:
#             print('===field=name===', field)
        
#             if field.name not in exclude_fields:
#                 print('==field==', field)
                
#                 if isinstance(field, models.ManyToManyField):
#                     # Handle ManyToMany fields separately
#                     related_objects = getattr(obj, field.name).all()  # This gets the related objects of the ManyToMany field
#                     print('===related objects===', related_objects)
                    
#                     # You can either store the related object's IDs, or serialize them based on your need
#                     related_object_ids = [related_obj.id for related_obj in related_objects]
#                     fields_and_values[field.name] = related_object_ids  # Store the IDs in the dictionary
#                 else:
#                     # For other field types, just store their value as usual
#                     fields_and_values[field.name] = getattr(obj, field.name)

#                 print('===fields_and_values after processing===', fields_and_values)

#         # Create an audit record
#         audit_model_name.objects.create(
#             audit_custom_record_id=generate_custom_record_id(record_id),
#             created_by=request.user,
#             updated_by=request.user,
#             **fields_and_values,
#             audit_status=status,
#         )
        
#         return True
#     except Exception as error:
#         error_log_v1(f"model_audit function raised an error: {error}")
#         return error

def model_audit(request,app_name,model_name,record_id,status='in_temp'):
    try:
      
        if status == 'in_temp':
            record = apps.get_model(app_name, f'{model_name}Temp')
        elif status == 'create' or status == 'update' or status == 'delete':
            record = apps.get_model(app_name, f'{model_name}Live')
        else:
            return False
        audit_model_name = apps.get_model(app_name, f'{model_name}Audit')
        obj = record.objects.get(pk=record_id)
        exclude_fields=['temp_status','temp_notes','is_deactivate','temp_record_type']
        fields_and_values = {
            field.name: getattr(obj, field.name)
            for field in obj._meta.fields
            if field.name not in exclude_fields
        }
        audit_model_name.objects.create(
            audit_custom_record_id=generate_custom_record_id(record_id),
            created_by=request.user,
            updated_by=request.user,
            **fields_and_values,
            audit_status=status,
        )
        return True
    except Exception as error:
        error_log_v1(f"model_audit  function raised an error: {error}")
        # print(f'model_audit getting {error}')
        return error
    

def self_authorization_for_delete(request,app_name,model_name, record_id,type):
    """
    Moves a specific record from a temporary model to a live model and deletes the temp record.

    Args:
        temp_model_name (str): The name of the temporary model from which records are to be moved.
        live_model_name (str): The name of the live model where the record should be moved.
        history_model_name (str): The name of the history model where the history should to recorded.
        record_id (int): The primary key of the record to be moved.

    Returns:
        bool: True if the operation was successful, False otherwise.

    Raises:
        Exception: Any error encountered during the process is caught and logged.
    """
    try:
        branch=request.user.branch
        model_reg = ModelRegistration.objects.filter(model_name=model_name,branch=branch).last()
        if model_reg:
            model=WorkflowMapping.objects.get(workflow_type=type,table_name=model_reg,branch=branch)
        
            if model.self_authorized:
                is_audit = model_audit(request,app_name,model_name,record_id,type)
                obj = delete_record(request,app_name,model_name, record_id)
                return obj
            return True
        else:
            error_log_v1("Model is not register")
            # print("Model is not register")
            return False
    except Exception as error:
        error_log_v1(f"move_record_temp_to_live delete  function raised an error: {error}")
        # print('move_record_temp_to_live delete function raised an error:', error)
        return False



#Create your views here.
def success(msg):
    # Create a dictionary named 'response' with two key-value pairs
    response={
        'status_code':0, # Key 'status_code' with value 0
        'data':msg       # Key 'data' with value 'msg' (the input parameter)
    }
    # Return the 'response' dictionary
    return response

def error(msg):
    # Create a dictionary with error details
    response={
        'status_code':1, # Status code indicating error
        'data':msg  # Error message
    }
    # Return the 'response' dictionary
    return response


