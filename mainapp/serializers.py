from rest_framework import serializers
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
        if instance.user.id and instance.user.first_name:
            rep["user"] = {
                'id': str(instance.user.id),
                'name': instance.user.first_name
            }
        else:
            rep["user"] = None
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
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        try:
            rep["client"] = instance.client.user.first_name
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
        fields = "__all__"

class FolderMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderMaster
        fields = "__all__"

class TRIOAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TRIOAssignment
        fields = "__all__"

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

class TRIOGroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TRIOGroupMember
        fields = "__all__"

class TRIOProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TRIOProfile
        fields = "__all__"

class FinalReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalReport
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

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

class TimesheetEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimesheetEntry
        fields = "__all__"

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

class MarketingAgentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingAgentProfile
        fields = "__all__"

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
