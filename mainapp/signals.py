from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import DocumentUpload, DocumentUploadHistory1, DocumentUploadAudit1

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
