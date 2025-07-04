from rest_framework import serializers

from user_management.serializers import UserSerializer
from .models import *

class UserTypeMasterSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserTypeMaster
		fields = "__all__"

class ScreenSerializer(serializers.ModelSerializer):
	class Meta:
		model = Screen
		fields = "__all__"
		
class ScreenVersionSerializer(serializers.ModelSerializer):
	class Meta:
		model = ScreenVersion
		fields = "__all__"

class ScreenVersionFieldsSerializer(serializers.ModelSerializer):
	class Meta:
		model = ScreenVersionFields
		fields = "__all__"

class ClientProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientProfile
        fields = "__all__"
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.user.user.id and instance.user.user.first_name:
            rep["user"] = {
                'id': str(instance.user.user.id),
                'name': instance.user.user.first_name
            }
            rep["user_id"]=instance.user.user.id
        else:
            rep["user"] = None
            rep["user_id"] = None
        return rep
    

class DocumentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentGroup
        fields = "__all__"

class CustomDocumentEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomDocumentEntity
        fields = "__all__"


class TaskTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTemplate
        fields = "__all__"
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        
        if instance.template:
            rep["template"] = {
                "id": instance.template.Template.id if instance.template.Template else None,
                "name": str(instance.template.Template.name) if instance.template.Template else None
            }
        else:
            rep["template"] = None
        return rep        
class TRIOGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TRIOGroup
        fields = "__all__"

class LoanCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanCase
        fields = "__all__"
        read_only_fields = ['case_id', 'case_reference']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        try:
            rep["client"] = {
                 "id":instance.client.user.user.id,
                 "name":instance.client.user.user.first_name
            }
        except AttributeError:
            rep["client"] = None
        return rep
    
    
class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = "__all__"

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'type']


class FolderMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderMaster
        fields = "__all__"

    def to_representation(self, instance):
        rep= super().to_representation(instance)
        if instance.client:
            rep['client']={
                'id':str(instance.client.user.user.id),
                'name':str(instance.client.user.user.first_name)
            }
        else:
            rep['client']=None

        return rep
class TRIOAssignmentSerializer(serializers.ModelSerializer):
    assigned_to=UserSerializer(many=True)
    class Meta:
        model = TRIOAssignment
        fields = "__all__"
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.group and instance.group.name:
            rep["group"] = {
                'id': str(instance.group.id),
                'name': instance.group.name
            }
        else:
            rep["group"] = None

        if instance.case and instance.case.case:
            rep["case"] = {
                'id': str(instance.case.id),
                'name': instance.case.case
            }
        else:
            rep["case"] = None
        if instance.assigned_by:
            rep["assigned_by"] = {
                'id': str(instance.assigned_by.id),
                'name': instance.assigned_by.first_name
            }
        else:
            rep["assigned_by"] = None
        
        return rep
class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = "__all__"

class ComplianceChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceChecklist
        fields = "__all__"

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        try:
            rep["case"] = {
                    'id': instance.case.id,
                    'name': instance.case.case
                        }
        except AttributeError:
            rep["case"] = None
        try:
            rep["uploaded_by"] = instance.uploaded_by.first_name
        except AttributeError:
            rep["uploaded_by"] = None
            
        try:
            rep["document_type"] = instance.document_type.type
        except AttributeError:
            rep["document_type"] = None
        return rep
    
class RiskAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskAssessment
        fields = "__all__"

class ClientQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientQuery
        fields = "__all__"

class TimeSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSheet
        fields = "__all__"

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentUpload
        fields = "__all__"
    

# class RequestDocumentSerializer(serializers.ModelSerializer):
#     document_type = DocumentTypeSerializer(many=True, read_only=True)

#     class Meta:
#         model = RequestDocument
#         fields = '__all__'

#     def to_representation(self, instance):
#         rep = super().to_representation(instance)

#         rep["requested_by"] = getattr(instance.requested_by, "first_name", None)

#         if instance.document_type.exists():
#             rep["document_type"] = ", ".join([dt.type for dt in instance.document_type.all()])
#         else:
#             rep["document_type"] = []
#         rep["case"] = {
#             "id": instance.case.id,
#             "name": instance.case.case
#         } if instance.case else None

#         return rep

class RequestDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestDocument
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep["requested_by"] = getattr(instance.requested_by, "first_name", None)
        rep["requested_to"] = getattr(instance.requested_to.user.user, "first_name", None)

        # Fix: use .all() before calling .exists() or iterating
        document_types = instance.document_type.all()
        if document_types.exists():
            rep["document_type"] = ", ".join([dt.type for dt in document_types])
        else:
            rep["document_type"] = ""

        rep["case"] = {
            "id": instance.case.id,
            "name": instance.case.case
        } if instance.case else None

        return rep
   

class DocumentUploadAudit1Serializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentUploadAudit1
        fields = "__all__"

class DocumentUploadHistory1Serializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentUploadHistory1
        fields = "__all__"

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.user and instance.user.first_name:
            rep["user"] = {
                'id': str(instance.user.id),
                'name': instance.user.first_name,
                'roles': instance.user.roles.name
            }
        else:
            rep["user"] = None

            
        return rep

class DocumentAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentAccess
        fields = "__all__"

class FileDownloadReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileDownloadReason
        fields = "__all__"

class CaseAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseAssignment
        fields = "__all__"
    def to_representation(self, instance):
        rep = super().to_representation(instance)
      
        try:
            profile_names = [p.user.first_name for p in instance.assigned_to.all() if p.user]
            rep["assigned_to"] = ", ".join(profile_names)
    
        except AttributeError:
            rep["assigned_to"] = None
        return rep    
class TRIOGroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TRIOGroupMember
        fields = "__all__"
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        try:
            rep["group"] = f"{instance.group.name} ({instance.group.get_enterprise_size_display()})"
        except AttributeError:
            rep["group"] = None
        try:
            profile_names = [p.user.first_name for p in instance.profile.all() if p.user]
            rep["profile"] = ", ".join(profile_names)
    
        except AttributeError:
            rep["profile"] = None
        return rep    
    
class TRIOProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TRIOProfile
        fields = "__all__"
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.user.id and instance.user.user.first_name:
            rep["user"] = {
                'id': str(instance.user.user.id),
                'name': instance.user.user.first_name
            }
            rep['user_id']=instance.user.user.id
        else:
            rep["user"] = None
            rep["user_id"] = None
        if instance.task_template:
            rep["task_template"] = {
                'id': str(instance.task_template.template.Template.id),
                'name': instance.task_template.template.Template.name
            }
        else:
            rep["task_template"] = None
        return rep
class FinalReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalReport
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.assignment.case.id and instance.assignment.case.case:
            rep["assignment"] = {
                'id': str(instance.assignment.case.id),
                'name': instance.assignment.case.case
            }
        else:
            rep["assignment"] = None
        if instance.template:
            rep["template"] = {
                'id': str(instance.template.template.Template.id),
                'name': instance.template.template.Template.name
            }
        else:
            rep["template"] = None
        if instance.assigned_to:
            rep["assigned_to"] = {
                'id': str(instance.assigned_to.user.user.id),
                'name': instance.assigned_to.user.user.first_name
            }
        else:
            rep["assigned_to"] = None
        return rep
class TaskAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAuditLog
        fields = "__all__"

class TaskDeliverableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDeliverable
        fields = "__all__"

class TaskTimesheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTimesheet
        fields = "__all__"
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.case.id and instance.case.case:
            rep["case"] = {
                'id': str(instance.case.id),
                'name': instance.case.case
            }
        else:
            rep["case"] = None
        if instance.employee.id :
            rep["employee"] = {
                'id': str(instance.employee.user.user.id),
                'name': instance.employee.user.user.first_name
            }
        else:
            rep["employee"] = None
        return rep
    

class TimesheetEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimesheetEntry
        fields = "__all__"
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.timesheet.id :
            rep["timesheet"] = {
                'id': str(instance.timesheet.id),
                'name': instance.timesheet.case.case
            }
        else:
            rep["employee"] = None
        return rep


class TimesheetEntryEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimesheetEntry
        fields = "__all__"
   

class TimesheetEntryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimesheetEntry
        fields = '__all__'

    # def update(self, instance, validated_data):
    #     request = self.context.get('request')

    #     # Check if new files are uploaded:
    #     new_document = request.FILES.get('document')
    #     new_attachment = request.FILES.get('attachment')

    #     if new_document:
    #         instance.document = new_document
    #     # Else, keep the old one:
    #     elif 'document' in validated_data:
    #         validated_data.pop('document')

    #     if new_attachment:
    #         instance.attachment = new_attachment
    #     elif 'attachment' in validated_data:
    #         validated_data.pop('attachment')

    #     # Update other fields:
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)

    #     instance.save()
    #     return instance


class TimesheetAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimesheetAttachment
        fields = "__all__"

class TimesheetDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimesheetDocument
        fields = "__all__"

class WorkScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSchedule
        fields = "__all__"

class TaskExtraHoursRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskExtraHoursRequest
        fields = "__all__"

class MeetingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meetings
        fields = "__all__"

class AuditorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditorProfile
        fields = "__all__"
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        try:
            rep["user"] = instance.user.user.first_name
            rep["user_id"] = instance.user.user.id
        except AttributeError:
            rep["user"] = None
            rep["user_id"] = None
        return rep
class MarketingAgentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingAgentProfile
        fields = "__all__"
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        try:
            rep["user"] = instance.user.user.first_name
            rep["user_id"] = instance.user.user.id
        except AttributeError:
            rep["user"] = None
            rep["user_id"] = None
        return rep

class IssueReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueReport
        fields = "__all__"

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"

class LawyerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawyerProfile
        fields = "__all__"
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        try:
            rep["user"] = instance.user.user.first_name
            rep["user_id"] = instance.user.user.id
        except AttributeError:
            rep["user"] = None
            rep["user_id"] = None
        return rep

class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = "__all__"

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = "__all__"

class StaffFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffFeedback
        fields = "__all__"

class TaskAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAssignment
        fields = "__all__"
