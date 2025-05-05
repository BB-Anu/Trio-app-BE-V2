from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import *
from django.utils import timezone
from datetime import timedelta
import re


@receiver(post_save, sender=DocumentUpload)
def create_document_history_and_audit(sender, instance, created, **kwargs):
    # Create DocumentUploadHistory1
    latest_version = DocumentUploadHistory1.objects.filter(document_id=instance.document_id).count() + 1
    DocumentUploadHistory1.objects.create(
        branch=instance.branch,
        document_id=instance.document_id,
        document_title=instance.document_title,
        document_type=instance.document_type,
        folder=instance.folder,
        document_size=instance.document_size,
        description=instance.description,
        document_upload=instance.document_upload,
        upload_date=instance.upload_date or now().date(),
        expiry_date=instance.expiry_date,
        start_date=instance.start_date,
        end_date=instance.end_date,
        version=latest_version
    )

    # Create DocumentUploadAudit1
    DocumentUploadAudit1.objects.create(
        branch=instance.branch,
        document_id=instance.document_id,
        document_title=instance.document_title,
        document_type=instance.document_type,
        folder=instance.folder,
        document_size=instance.document_size,
        description=instance.description,
        document_upload=instance.document_upload,
        upload_date=instance.upload_date or now().date(),
        expiry_date=instance.expiry_date,
        start_date=instance.start_date,
        end_date=instance.end_date,
        status='created' if created else 'updated',
        created_by=instance.created_by,
        updated_by=instance.update_by
    )

@receiver(post_save, sender=LoanCase)
def assign_case_based_on_enterprise_size(sender, instance, created, **kwargs):
    if created and instance.client.enterprise_size:
        entity=CustomDocumentEntity.objects.get(client=instance.client)
        FolderMaster.objects.create(
        branch=instance.branch if hasattr(instance, 'branch') else None,
        folder_id= f"ENT-{instance.id}",
        folder_name=f"ENT-{instance.case}-{instance.case_id}",
        case=instance,
        description = f"Created for {instance.case}",
        entity=entity,
        client = instance.client,
        created_by =instance.created_by,
        )
        enterprise_size = instance.client.enterprise_size  # NANO, MICRO, etc.
        print('enterprise_size,',enterprise_size)
        try:
            # Get users in the group matching the enterprise size
            group = TRIOGroup.objects.filter(enterprise_size=enterprise_size,is_available=True).first()
            print('----',group)
            group_members = TRIOGroupMember.objects.filter(group=group)

            # Collect all user profiles from all group members
            user_profiles = UserProfile.objects.filter(
                triogroupmember__in=group_members
            ).distinct()

            print('--users_in_group--', user_profiles)

            if user_profiles.exists():
                # Extract corresponding User instances
                users = [profile.user for profile in user_profiles if profile.user]

                # Create the case assignment
                case_assignment = TRIOAssignment.objects.create(
                    case=instance,
                    branch=instance.branch,
                    group=group,
                    assigned_by=instance.created_by,
                )

                # Assign the users to the assignment
                case_assignment.assigned_to.set(users)
                case_assignment.save()
                group.is_available=False
                group.save()
                for user_profile in user_profiles:
                    user = user_profile.id
                    print('user',user)
                    try:
                        trio_profile = TRIOProfile.objects.get(user=user)
                        print("TRIOProfile found:", trio_profile)
                        template=trio_profile.task_template
                        task_temp=TaskTemplate.objects.get(id=template.id)
                        print(task_temp.checklist)
                        allocated_hours=task_temp.hours_allocated
                        print('template',template)
                        if not template:
                            continue
                        checklist_items = [item.strip() for item in template.checklist.split('\n') if item.strip()]
                        print('checklist_items',checklist_items)
                        hours_required = allocated_hours
                        days_required = hours_required / 8
                        due_date = instance.start_date + timedelta(days=days_required)

                        for item in checklist_items:
                            Task.objects.create(
                                branch=instance.branch,
                                assignment=case_assignment,
                                template=template,
                                assigned_to=trio_profile,
                                due_date=due_date,
                                status='pending',
                                task_description=item
                            )
                        # Divide total hours equally among checklist items
                            total_hours = allocated_hours
                            # # For each checklist item, create a separate task
                            # for item in checklist_items:
                            #     # Divide total hours equally among checklist items
                            #     per_task_hours = round(total_hours / len(checklist_items), 2)

                            #     # Create a separate TaskTimesheet entry for each checklist item
                            #     TaskTimesheet.objects.create(
                            #         branch=instance.branch,
                            #         employee=trio_profile,
                            #         task=item,  # This is the individual checklist item text
                            #         date=instance.start_date,  # Use the start date or timezone.now().date()
                            #         total_working_hours=per_task_hours,
                            #         hours_spent=0.0,
                            #         remarks="Auto-created task from checklist"
                            #     )

                        checklist_items = [
                            item.strip()
                            for item in re.split(r'(?<=[.])\s+(?=[A-Z])', template.checklist.strip())
                            if item.strip()
                        ]
                        print('Checklist Items:', checklist_items)

                        total_hours = task_temp.hours_allocated
                        per_task_hours = round(total_hours / len(checklist_items), 2)
                        days_required = round(total_hours / 8, 2)
                        due_date = instance.start_date + timedelta(days=days_required)
                        for item in checklist_items:
                            # Create Task once per checklist item
                            # task_obj = Task.objects.create(
                            #     branch=instance.branch,
                            #     assignment=case_assignment,
                            #     template=template,
                            #     assigned_to=trio_profile,
                            #     due_date=due_date,
                            #     status='pending',
                            #     task_description=item
                            # )

                            # Create TaskTimesheet for the created Task
                            TaskTimesheet.objects.create(
                                branch=instance.branch,
                                employee=trio_profile,
                                task=item,  # Optional: use `task=task_obj` if FK
                                case=instance,
                                date=instance.start_date,
                                total_working_hours=per_task_hours,
                                hours_spent=0.0,
                                remarks="Auto-created task from checklist"
                            )
                        # Example: create tasks, assign etc.
                        # Task.objects.create(
                        #     branch=instance.branch,
                        #     assignment=case_assignment,
                        #     template=trio_profile.task_template,
                        #     assigned_to=trio_profile,
                        #     due_date=timezone.now().date() + timedelta(days=7),
                        #     status='pending'
                        # )

                    except TRIOProfile.DoesNotExist:
                        print(f"TRIOProfile not found for user {user}")
                        continue
        except TRIOGroup.DoesNotExist:
            pass

            
@receiver(post_save, sender=ClientProfile)
def create_customdocument_entity(sender, instance, created, **kwargs):
    if created:
        entity_id = f"ENT-{instance.id}"
        entity_name = f"{instance.business_name}"  
        CustomDocumentEntity.objects.create(
        branch=instance.branch if hasattr(instance, 'branch') else None,
        entity_id=entity_id,
        entity_name=entity_name,
        entity_type="Client",  
        client=instance,
        description=f"Auto-created entity for {instance} profile"
        )
        
        