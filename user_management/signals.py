from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from user_management.models import User, Branch
from mainapp.models import FolderMaster, CustomDocumentEntity, DocumentType
import uuid

@receiver(post_save, sender=User)
def create_default_folders_for_user(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance
    role = getattr(user, 'roles', None)  # adjust if ManyToMany or FK

    # Defaults
    default_branch = getattr(user, 'branch', None) or Branch.objects.first()
    default_entity = CustomDocumentEntity.objects.filter(entity_name='Default Entity').first()

    if not default_branch or not default_entity:
        # Log or handle error as needed
        return

    # Define folder names and optionally associated document types
    role_folders = {
        'Auditor': [('Auditor Docs', 'Reports')],
        'customer': [('Client Uploads', 'KYC Document'), ('KYC Documents', 'KYC Document')],
        'Lawyer': [('Legal Reviews', 'Agreement')],
        'Marketing Agent': [('Marketing Docs', 'Loan Application')],
    }

    folders = role_folders.get(role, [('General Folder', None)])

    for folder_name, doc_type_name in folders:
        unique_id = uuid.uuid4().hex[:6]
        folder_id = f"{slugify(user.first_name)}_{slugify(folder_name)}_{unique_id}"

        # Avoid duplicates
        if FolderMaster.objects.filter(folder_id=folder_id).exists():
            continue

        folder = FolderMaster.objects.create(
            branch=default_branch,
            folder_id=folder_id,
            folder_name=folder_name,
            description=f"Auto-created folder for {role or 'General'}",
            entity=default_entity,
            client=None,
            created_by=user,
            update_by=user,
        )

        # Optional: Tag with document type
        if doc_type_name:
            doc_type = DocumentType.objects.filter(title__icontains=doc_type_name).first()
            if doc_type:
                # You can optionally link the document type to folder if you have such a relation
                pass  # or folder.document_types.add(doc_type) if such M2M exists
