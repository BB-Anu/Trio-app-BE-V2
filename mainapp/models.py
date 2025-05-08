from django.core.validators import MinValueValidator,FileExtensionValidator,MaxValueValidator
from django.db import models
from datetime import datetime
from django.utils.timezone import now
from user_management.models import Branch

class Screen(models.Model):
    screen_name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.screen_name 
    
class UserTypeMaster(models.Model):
    user_type=models.CharField(max_length=50)
    description=models.TextField()
    def __str__(self) -> str:
        return self.user_type
    
class ScreenVersion(models.Model):
    verion_name=models.CharField(max_length=50)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    user_type = models.ForeignKey(UserTypeMaster, on_delete=models.CASCADE)
    status=models.CharField(max_length=10, default="pending")
    def __str__(self) -> str:
        return self.verion_name
    
class ScreenVersionFields(models.Model):
    version = models.ForeignKey(ScreenVersion, on_delete=models.CASCADE)
    field = models.CharField(max_length=50, blank=True,null=True)
    column_size = models.IntegerField()
    label_name = models.CharField(max_length=50, blank=True,null=True)
    position = models.IntegerField(blank=True, null=True)

# Profiles for Stakeholders


class UserProfile(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	user = models.OneToOneField('user_management.User', on_delete=models.CASCADE, blank=True, null=True, related_name="%(class)s_user")
	# role = models.ForeignKey('user_management.Role', on_delete=models.CASCADE, related_name="%(class)s_role", blank=True, null=True)
	phone = models.CharField(max_length=250,blank=True, null=True ,)
	email = models.EmailField()
	profile_completed = models.BooleanField()
	status = models.CharField(max_length=250,choices=[ ('pending', 'pending'), ('Completed', 'Completed')],default='pending')



class ClientProfile(models.Model):
	ENTERPRISE_SIZE_CHOICES = [
		('NANO', 'Nano Enterprise'),
		('MICRO', 'Micro Enterprise'),
		('SMALL', 'Small Enterprise'),
		('MEDIUM', 'Medium Enterprise'),
	]
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	user = models.OneToOneField('user_management.User', on_delete=models.CASCADE, related_name="%(class)s_user")
	business_name = models.CharField(max_length=250,)
	business_type = models.CharField(max_length=250,)
	registration_number = models.CharField(max_length=250,)
	kra_pin = models.CharField(max_length=250,)
	contact_email = models.EmailField()
	contact_phone = models.CharField(max_length=250,)
	address = models.TextField()
	tax_compliance_cert = models.FileField(upload_to="documents/", validators=[FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"])], blank=True, null=True)
	number_of_employees = models.PositiveIntegerField(null=True, blank=True)
	annual_turnover = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
	enterprise_size = models.CharField(max_length=10, choices=ENTERPRISE_SIZE_CHOICES, null=True, blank=True)
	def save(self, *args, **kwargs):
		if self.number_of_employees is not None:
			if self.number_of_employees <= 10:
				self.enterprise_size = 'NANO'
			elif self.number_of_employees <= 50:
				self.enterprise_size = 'MICRO'
			elif self.number_of_employees <= 250:
				self.enterprise_size = 'SMALL'
			else:
				self.enterprise_size = 'MEDIUM'
		super(ClientProfile, self).save(*args, **kwargs)
	def __str__(self):
		return self.business_name

class AuditorProfile(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	user = models.OneToOneField('user_management.User', on_delete=models.CASCADE, related_name="%(class)s_user")
	firm_name = models.CharField(max_length=250,)
	license_number = models.CharField(max_length=250,)
	years_of_experience = models.PositiveIntegerField()
	qualifications = models.TextField(blank=True, null=True,)
	accreditation_body = models.CharField(max_length=250,blank=True, null=True ,)
	contact_phone = models.CharField(max_length=250,)
	contact_email = models.EmailField()
	address = models.TextField()
	is_internal = models.BooleanField()
	nda_signed = models.BooleanField()
	active = models.BooleanField()
	def __str__(self):
		return self.firm_name

class MarketingAgentProfile(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	user = models.OneToOneField('user_management.User', on_delete=models.CASCADE, related_name="%(class)s_user")
	agency_name = models.CharField(max_length=250,blank=True, null=True ,)
	expertise_area = models.CharField(max_length=250,)
	years_of_experience = models.PositiveIntegerField()
	market_sector_focus = models.CharField(max_length=250,blank=True, null=True ,)
	contact_phone = models.CharField(max_length=250,)
	contact_email = models.EmailField()
	address = models.TextField()
	has_ndasigned = models.BooleanField()
	available_for_assignment = models.BooleanField()
	def __str__(self):
		return self.agency_name

class LawyerProfile(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	user = models.OneToOneField('user_management.User', on_delete=models.CASCADE, related_name="%(class)s_user")
	law_firm = models.CharField(max_length=250,)
	bar_registration_number = models.CharField(max_length=250,)
	specialization_area = models.CharField(max_length=250,)
	years_of_practice = models.PositiveIntegerField()
	qualifications = models.TextField(blank=True, null=True,)
	contact_phone = models.CharField(max_length=250,)
	contact_email = models.EmailField()
	address = models.TextField()
	licensed = models.BooleanField()
	nda_signed = models.BooleanField()
	active = models.BooleanField()
	def __str__(self):
		return self.law_firm

class TRIOProfile(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="%(class)s_profile_user")
	# role = models.ForeignKey('user_management.Role', on_delete=models.CASCADE, related_name="%(class)s_role", blank=True, null=True)
	task_template=models.ForeignKey('TaskTemplate', on_delete=models.CASCADE, related_name="%(class)s_tasktemplate",null=True,blank=True)
	qualification = models.TextField()
	experience_years = models.IntegerField()
	phone = models.IntegerField()
	is_active = models.BooleanField()
	
class Members(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	email = models.EmailField()
	password = models.CharField(max_length=250,)
	otp = models.CharField(max_length=250,)
	def __str__(self):
		return self.email
	
# Loan Case Management
class LoanCase(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
	case = models.CharField(max_length=250,blank=True,)
	case_id = models.CharField(max_length=250,unique=True)
	case_reference = models.CharField(max_length=250,unique=True)
	loan_amount = models.DecimalField(max_digits=10, decimal_places=2,)
	loan_purpose = models.TextField()
	created_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE, related_name="%(class)s_case",blank=True, null=True)
	created_at = models.DateTimeField(auto_now=True)
	start_date = models.DateTimeField(null=True,blank=True)
	status = models.CharField(max_length=40, choices=[ ('new', 'New'),('info_gathering', 'Information Gathering'), ('in_progress', 'Under Analysis'), ('review', 'Under Review'),('rework', 'Rework'), ('approved', 'Approved'), ('declined', 'Declined'),  ('closed', 'Closed'),    ], default='new')
	def save(self, *args, **kwargs):
		if not self.case_id:
			last_id = LoanCase.objects.aggregate(models.Max('id'))['id__max'] or 0
			next_id = last_id + 1
			self.case_id = f"CASE{next_id:04d}"       # e.g. CASE0001
			self.case_reference = f"REF{next_id:04d}"  # e.g. REF0001
		super().save(*args, **kwargs)
	def __str__(self):
		return f"{self.case_reference} - {self.client.business_name}"

class CaseAssignment(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	case = models.ForeignKey(LoanCase, on_delete=models.CASCADE)
	user = models.ForeignKey('user_management.User', on_delete=models.CASCADE)
	assigned_to = models.ManyToManyField('UserProfile', blank=True)
	# role = models.CharField(max_length=250,)
	assigned_at = models.DateField(auto_now=True)
	due_date = models.DateField()
	status = models.CharField(max_length=250,choices=[ ('pending', 'pending'), ('Completed', 'Completed')],default='pending')
	def __str__(self):
		return f"Case: {self.case}, Assigned To: {[user.id for user in self.assigned_to.all()]}"
	

class Document(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	case = models.ForeignKey(LoanCase, on_delete=models.CASCADE)
	uploaded_by = models.ForeignKey('user_management.User', on_delete=models.SET_NULL, null=True)
	document_type = models.CharField(max_length=250,)
	file = models.FileField(upload_to="documents/", validators=[FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"])],null=True, blank=True )
	version = models.IntegerField()
	uploaded_at = models.DateTimeField(auto_now_add=True)
	status=models.CharField(max_length=10,choices=[('pending','pending'),('approved','approved'),('rejected','rejected')],default='pending')
	reject_reason= models.CharField(max_length=250,null=True,blank=True)
	def __str__(self):
		return self.document_type

class ComplianceChecklist(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	case = models.ForeignKey(LoanCase, on_delete=models.CASCADE)
	item_name = models.CharField(max_length=250,)
	is_verified = models.BooleanField()
	verified_by = models.ForeignKey('user_management.User', on_delete=models.SET_NULL, null=True, blank=True)
	verified_at = models.DateTimeField(blank=True, null=True,)
	def __str__(self):
		return self.case

#  Document Management & Messaging

class CustomDocumentEntity(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	entity_id = models.CharField(max_length=250,)
	entity_name = models.CharField(max_length=250,)
	entity_type = models.CharField(max_length=250,)
	client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, blank=True, null=True,related_name='%(class)s_client')
	description = models.TextField(blank=True, null=True,)
	def __str__(self):
		return self.entity_id
	
class FolderMaster(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	folder_id=models.CharField(max_length=100, unique=True,blank=False,null=False)
	folder_name=models.CharField(max_length=100,blank=False,null=False)
	description = models.TextField(max_length=500,blank=True, null=True)
	entity=models.ForeignKey(CustomDocumentEntity, on_delete=models.CASCADE)
	client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, blank=True, null=True,related_name='%(class)s_client')
	case = models.ForeignKey(LoanCase, on_delete=models.CASCADE,blank=True, null=True,related_name='%(class)s_case')
	master_checkbox_file = models.BooleanField(default=False, blank=True, null=True)
	parent_folder=models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='FolderMasters')
	default_folder=models.BooleanField(default=False)
	created_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE,related_name="FolderMastere1_created_by",blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	update_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE, blank=True, null=True,related_name="FolderMastere1_update_by")
	update_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.folder_id

class DocumentGroup(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	group_name = models.CharField(max_length=255,unique=False ,)
	description=models.CharField(max_length=255,null=True)
	created_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE, related_name="%(class)s_created_by", blank=True, null=True)  
	created_at = models.DateTimeField(auto_now_add=True) 
	updated_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE, blank=True, null=True, related_name="%(class)s_updated_by")  
	updated_at = models.DateTimeField(auto_now=True)  
	def __str__(self):
		return self.group_name

class DocumentType(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	type = models.CharField(max_length=255,unique=False ,)
	description = models.CharField(max_length=255,unique=False ,)
	# group= models.ForeignKey(DocumentGroup, on_delete=models.CASCADE, related_name='%(class)s_group')
	created_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE, related_name="%(class)s_created_by", blank=True, null=True)  
	created_at = models.DateTimeField(auto_now_add=True) 
	updated_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE, blank=True, null=True, related_name="%(class)s_updated_by")  
	updated_at = models.DateTimeField(auto_now=True)  
	def __str__(self):
		return self.type

class DocumentUpload(models.Model):	
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	document_id=models.CharField(max_length=100, primary_key=True)
	document_title=models.CharField(max_length=100,blank=False,null=False)
	document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, related_name='%(class)s_document_type')
	entity_type=models.ManyToManyField(CustomDocumentEntity,blank=True)
	folder=models.ForeignKey(FolderMaster,on_delete=models.CASCADE,blank=True, null=True)
	document_size=models.PositiveBigIntegerField(blank=True,null=True)
	description = models.TextField(blank=True, null=True)
	document_upload = models.FileField(upload_to="DMS/",blank=True, null=True)
	upload_date = models.DateField(blank=True, null=True, auto_now_add=True)
	expiry_date= models.DateField(blank=True,null=True)
	start_date=models.DateField(blank=True,null=True)
	end_date=models.DateField(blank=True,null=True)
	created_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE,related_name="DocumentUpload1_created_by" , blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	update_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE, blank=True, null=True,related_name="DocumentUpload1_update_by")
	update_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.document_id

class DocumentUploadHistory1(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	document_id=models.CharField(max_length=100,blank=False,null=False)
	document_title=models.CharField(max_length=100,blank=False,null=False)
	document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, related_name='%(class)s_document_type')
	folder=models.ForeignKey(FolderMaster,on_delete=models.CASCADE,blank=True, null=True)
	document_size=models.PositiveBigIntegerField(blank=True,null=True)
	description = models.TextField(blank=True, null=True)
	document_upload = models.FileField(blank=True, null=True)
	upload_date = models.DateField(blank=True, null=True, default=now)
	expiry_date= models.DateField(blank=True,null=True)
	start_date=models.DateField(blank=True,null=True)
	end_date=models.DateField(blank=True,null=True)
	is_deactivate = models.BooleanField(default=False)
	version = models.PositiveIntegerField()
	def __str__(self):
		return self.document_id
	
class DocumentUploadAudit1(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	document_id=models.CharField(max_length=100,blank=False,null=False)
	document_title=models.CharField(max_length=100,blank=False,null=False)
	document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, related_name='%(class)s_document_type')
	folder=models.ForeignKey(FolderMaster,on_delete=models.CASCADE,blank=True, null=True)
	document_size=models.PositiveBigIntegerField(blank=True,null=True)
	description = models.TextField(blank=True, null=True)
	document_upload = models.FileField(blank=True, null=True)
	upload_date = models.DateField(blank=True, null=True, default=now)
	expiry_date= models.DateField(blank=True,null=True)
	start_date=models.DateField(blank=True,null=True)
	end_date=models.DateField(blank=True,null=True)
	status = models.CharField(max_length=100, choices=[ ('created', 'Created'), ('updated', 'Updated'),('deleted', 'Deleted'),])
	created_by = models.ForeignKey('user_management.User', related_name='DocumentUploadAuditAudit1_created_by', on_delete=models.SET_NULL,null=True)
	updated_by = models.ForeignKey('user_management.User', related_name='DocumentUploadAuditAudit1_updated_by', on_delete=models.SET_NULL,null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.document_id

class DocumentAccess(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	document = models.ForeignKey(DocumentUpload,on_delete=models.CASCADE)
	access_to = models.ForeignKey('user_management.User', on_delete=models.CASCADE,related_name="DocumentAccess_access_to")
	permission = models.TextField(blank=True,null=True)
	expiry_from_at = models.DateTimeField(blank=True,null=True)
	expiry_to_at = models.DateTimeField(blank=True,null=True)
	created_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE,blank=True, null=True,related_name="DocumentAccess1_created_by")
	created_at = models.DateTimeField(auto_now_add=True)
	update_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE, blank=True, null=True,related_name="DocumentAccess1_update_by")
	update_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.document
	
class FileDownloadReason(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	document = models.ForeignKey(DocumentUpload,on_delete=models.CASCADE,related_name="FileDownloadReason")
	reason = models.TextField()
	created_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE,related_name="FileDownloadReason_created_by", blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	update_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE, blank=True, null=True,related_name="FileDownloadReason_update_by")
	update_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.document
	
#   Task & Deliverables Management
class TaskTemplate(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	template = models.ForeignKey('task.TemplateDocument', on_delete=models.CASCADE, null=True, blank=True)
	title = models.CharField(max_length=250,)
	description = models.TextField()
	hours_allocated = models.FloatField()
	checklist = models.TextField()
	deliverables = models.TextField()
	def __str__(self):
		return self.title

class TRIOGroup(models.Model):
	ENTERPRISE_SIZE_CHOICES = [
		('NANO', 'Nano Enterprise'),
		('MICRO', 'Micro Enterprise'),
		('SMALL', 'Small Enterprise'),
		('MEDIUM', 'Medium Enterprise'),
	]
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=100)
	enterprise_size = models.CharField(max_length=10, choices=ENTERPRISE_SIZE_CHOICES, null=True, blank=True)
	created_by = models.ForeignKey('user_management.User', on_delete=models.SET_NULL, null=True)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	is_available=models.BooleanField(default=True)
	def __str__(self):
		return self.name

class TRIOGroupMember(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	group = models.ForeignKey(TRIOGroup, on_delete=models.CASCADE)
	profile = models.ManyToManyField(UserProfile, blank=True)
	def __str__(self):
		return self.group

class TRIOAssignment(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	# customer = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
	case = models.ForeignKey(LoanCase, on_delete=models.CASCADE,blank=True,null=True,related_name='assignment')
	group = models.ForeignKey(TRIOGroup, on_delete=models.CASCADE)
	assigned_by = models.ForeignKey('user_management.User', on_delete=models.SET_NULL, null=True,related_name='assign_by')
	assigned_to = models.ManyToManyField('user_management.User',related_name='assign_to')
	assigned_on = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f'{self.case}-{self.group}'

class Task(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	assignment = models.ForeignKey(TRIOAssignment, on_delete=models.CASCADE)
	template = models.ForeignKey(TaskTemplate, on_delete=models.SET_NULL, null=True)
	task_description=models.CharField(max_length=250,null=True,blank=True)
	assigned_to = models.ForeignKey('TRIOProfile', on_delete=models.SET_NULL, null=True)
	due_date = models.DateField()
	status = models.CharField(max_length=20, choices=[
		('pending', 'Pending'),
		('in_progress', 'In Progress'),
		('completed', 'Completed')
	], default='pending')
	def __str__(self):
		return f"Task for {self.assignment.customer.business_name} (Assigned to {self.assigned_to.user})"
	

class TaskDeliverable(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	file = models.FileField(upload_to='deliverables/')
	description = models.TextField()
	uploaded_on = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.task

class TaskTimesheet(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	employee = models.ForeignKey(TRIOProfile, on_delete=models.CASCADE, related_name='%(class)s_employee')
	case = models.ForeignKey(LoanCase, on_delete=models.CASCADE,null=True,blank=True)
	task = models.CharField(max_length=255,null=True,blank=True)
	date = models.DateField()
	total_working_hours = models.FloatField(null=True,blank=True)
	hours_spent = models.FloatField(default=0.0)
	remarks = models.TextField(blank=True)
	status=models.CharField(max_length=20,choices=[('pending','pending'),('completed','completed'),('approved','approved'),('rejected','rejected')],default='pending')
	def __str__(self):
		return str(self.id) 

class FinalReport(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	assignment = models.ForeignKey(TRIOAssignment, on_delete=models.CASCADE)
	report_title = models.CharField(max_length=255)
	content = models.TextField()
	submitted_on = models.DateTimeField(auto_now_add=True)
	submitted_by = models.ForeignKey('TRIOProfile', on_delete=models.SET_NULL, null=True)
	def __str__(self):
		return self.assignment

class TaskAuditLog(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='audit_logs')
	message = models.TextField() 
	created_by = models.ForeignKey('user_management.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='task_audit_created_by')
	created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
	updated_by = models.ForeignKey('user_management.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='task_audit_updated_by')
	updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
	def __str__(self):
		return self.task

#  Risk Assessment
class RiskAssessment(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	case = models.OneToOneField(LoanCase, on_delete=models.CASCADE, related_name="%(class)s_case")
	analyst = models.ForeignKey('user_management.User', on_delete=models.SET_NULL, null=True)
	score = models.IntegerField()
	grade = models.CharField(max_length=250,)
	summary = models.TextField()
	recommendation = models.CharField(max_length=250,)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.analyst

#  NMSE Report & Approval
#  Compliance & Audit Trail
class AuditLog(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	user = models.ForeignKey('user_management.User', on_delete=models.SET_NULL, null=True)
	action = models.CharField(max_length=255)
	timestamp = models.DateTimeField(auto_now_add=True)
	case = models.ForeignKey(LoanCase, on_delete=models.CASCADE, null=True, blank=True)
	meta = models.JSONField(blank=True, null=True)
	def __str__(self):
		return self.user

# LoanCase, RiskAssessment, Task, TimesheetEntry, ClientQuery
#  Notifications & Feedback
class Notification(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=250,)
	msg = models.CharField(max_length=250,)
	created_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE, related_name="notification_created_by", blank=True, null=True)  
	updated_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE, blank=True, null=True, related_name="notification_updated_by")  
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.name
	
class StaffFeedback(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	staff = models.ForeignKey('user_management.User', on_delete=models.CASCADE, related_name='staff_feedbacks')
	feedback = models.TextField()
	rating = models.PositiveIntegerField()
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	filename = models.CharField(max_length=250,blank=True, null=True ,)
	file_type = models.CharField(max_length=250,blank=True, null=True ,)
	def __str__(self):
		return self.staff
	
# Issue Tracking & Internal Tasks
class IssueReport(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	staff = models.ForeignKey('user_management.User', on_delete=models.CASCADE, related_name='reported_issues',blank=True, null=True,)
	description = models.TextField(blank=True, null=True,)
	screen_name = models.CharField(max_length=250,blank=True, null=True ,)
	status = models.CharField(max_length=250, choices=[  ('open', 'Open'), ('assigned', 'Assigned'),('resolved', 'Resolved'),], default='open',blank=True, null=True ,)
	filename = models.CharField(max_length=250,blank=True, null=True ,)
	file_type = models.CharField(max_length=250,blank=True, null=True ,)
	created_at = models.DateTimeField(blank=True, null=True,)
	updated_at = models.DateTimeField(blank=True, null=True,)
	def __str__(self):
		return self.staff
	

class TaskAssignment(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	issue = models.OneToOneField(IssueReport, on_delete=models.CASCADE, blank=True, null=True, related_name="%(class)s_issue")
	assigned_to = models.ForeignKey('user_management.User', on_delete=models.CASCADE, related_name='assigned_tasks',blank=True, null=True,)
	assigned_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE, related_name='assigned_by',blank=True, null=True,)
	assigned_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
	due_date = models.DateField(blank=True, null=True,)
	notes = models.TextField(blank=True, null=True,)
	def __str__(self):
		return self.assigned_to

# Timesheets & Work Tracking
class Projects(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	project_name = models.CharField(max_length=255,unique=False ,)
	client = models.ManyToManyField(UserProfile, blank=True)
	start_date = models.DateField()
	end_date = models.DateField(blank=True, null=True,)
	status = models.CharField(max_length=250,)
	def __str__(self):
		return self.project_name

class TimeSheet(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	employee = models.ForeignKey('user_management.User', on_delete=models.CASCADE, related_name='%(class)s_employee')
	project= models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='%(class)s_project')
	date = models.DateField()
	total_working_hours = models.FloatField(null=True,blank=True)
	working_hours = models.FloatField(null=True,blank=True)
	status = models.CharField(max_length=50,choices=[('Pending', 'Pending'),('Completed', 'Completed'),('Approved', 'Approved'),('Rejected', 'Rejected')],default='Pending',null=True,blank=True)
	location = models.TextField(blank=True, null=True,)
	created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
	def __str__(self):
		return self.employee

class TimesheetEntry(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	timesheet= models.ForeignKey(TaskTimesheet, on_delete=models.CASCADE, related_name='%(class)s_timesheet')
	task= models.ForeignKey(Task, on_delete=models.CASCADE, related_name='%(class)s_task',blank=True, null=True)
	hours = models.FloatField()
	work_done = models.TextField()
	uploaded_at = models.DateTimeField(auto_now_add=True)
	document = models.BinaryField(blank=True, null=True)
	filename = models.CharField(max_length=255, blank=True, null=True) 
	file_type = models.CharField(max_length=255, blank=True, null=True)  
	attachment = models.BinaryField(blank=True, null=True)
	attachment_name = models.CharField(max_length=255, blank=True, null=True)  
	attachment_type = models.CharField(max_length=255, blank=True, null=True)
	is_late_hours = models.BooleanField(default=False,blank=True, null=True)
	is_wfh_hours = models.BooleanField(default=False,blank=True, null=True)
	payment_status = models.CharField(max_length=50,choices=[('Pending', 'Pending'),('Paid', 'Paid'),('UnPaid', 'UnPaid')],default='Pending',null=True,blank=True)
	approved_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE, related_name="%(class)s_approved_by", blank=True, null=True)  
	status = models.CharField(max_length=50,choices=[('Pending', 'Pending'),('Completed', 'Completed'),('Approved', 'Approved'),('Rejected', 'Rejected')],default='Pending',null=True,blank=True)
	created_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE, related_name="%(class)s_created_by", blank=True, null=True)  
	created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
	def __str__(self):
		return self.id
	
class TimesheetDocument(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	entry = models.ForeignKey(TimesheetEntry, related_name='documents', on_delete=models.CASCADE)
	document = models.BinaryField(blank=True,null=True)
	filename = models.CharField(max_length=255)
	file_type = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.entry
	
class TimesheetAttachment(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	entry = models.ForeignKey(TimesheetEntry, related_name='entry_documents', on_delete=models.CASCADE)
	attachment = models.BinaryField(blank=True,null=True)
	filename = models.CharField(max_length=250,)
	file_type = models.CharField(max_length=250,)
	created_at = models.DateTimeField()
	def __str__(self):
		return self.entry

class TaskExtraHoursRequest(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	task= models.ForeignKey(Task, on_delete=models.CASCADE, related_name='%(class)s_task',blank=True, null=True,)
	employee = models.ForeignKey('user_management.User', on_delete=models.CASCADE, related_name='%(class)s_employee',blank=True, null=True,)
	approved=models.BooleanField(default=False, blank=True, null=True)
	extra_hours=models.PositiveBigIntegerField(null=True,blank=True)
	reason=models.TextField(blank=True, null=True,)
	created_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE, related_name="%(class)s_created_by", blank=True, null=True)  
	created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True,) 
	updated_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE, blank=True, null=True, related_name="%(class)s_updated_by")  
	updated_at = models.DateTimeField(auto_now=True,blank=True, null=True,)  
	def __str__(self):
		return self.task

class WorkSchedule(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	monday = models.CharField(max_length=10, choices= [("Full Day", "Full Day"), ("Half Day", "Half Day"), ("Weekend", "Weekend")], default="Full Day",null=True, blank=True)
	tuesday = models.CharField(max_length=10, choices= [("Full Day", "Full Day"), ("Half Day", "Half Day"), ("Weekend", "Weekend")], default="Full Day",null=True, blank=True)
	wednesday = models.CharField(max_length=10, choices= [("Full Day", "Full Day"), ("Half Day", "Half Day"), ("Weekend", "Weekend")], default="Full Day",null=True, blank=True)
	thursday = models.CharField(max_length=10, choices= [("Full Day", "Full Day"), ("Half Day", "Half Day"), ("Weekend", "Weekend")], default="Full Day",null=True, blank=True)
	friday = models.CharField(max_length=10, choices= [("Full Day", "Full Day"), ("Half Day", "Half Day"), ("Weekend", "Weekend")], default="Full Day",null=True, blank=True)
	saturday = models.CharField(max_length=10, choices= [("Full Day", "Full Day"), ("Half Day", "Half Day"), ("Weekend", "Weekend")], default="Weekend",null=True, blank=True)
	sunday = models.CharField(max_length=10, choices= [("Full Day", "Full Day"), ("Half Day", "Half Day"), ("Weekend", "Weekend")], default="Weekend",null=True, blank=True)
	created_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE, related_name="%(class)s_created_by", blank=True, null=True)  
	created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
	def __str__(self):
		return self.monday
	
#  Meetings & Events
class Meetings(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	title = models.CharField(max_length=255,blank=True, null=True ,)
	location = models.CharField(max_length=255,blank=True, null=True ,)
	attendees = models.ManyToManyField('user_management.User', related_name='%(class)s_attendees')
	purpose = models.TextField(blank=True, null=True,)
	meeting_agenda = models.TextField(blank=True, null=True,)
	meeting_notes = models.TextField(blank=True, null=True,)
	meeting_date = models.DateField()
	meeting_time = models.TimeField(blank=True,null=True)
	delivery_date = models.DateField(blank=True, null=True,)
	document = models.BinaryField(blank=True, null=True)
	filename = models.CharField(max_length=255, blank=True, null=True)  
	file_type = models.CharField(max_length=255, blank=True, null=True) 
	secretary = models.ForeignKey('user_management.User', on_delete=models.CASCADE, related_name="%(class)s_secretary", blank=True, null=True)  
	status = models.CharField(max_length=50,choices=[('Scheduled', 'Scheduled'), ('ReScheduled', 'ReScheduled'),('Cancelled','Cancelled'),('Closed','Closed')],default='Scheduled')
	reschedule_reason=models.CharField(max_length=100,null=True,blank=True)
	created_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE, related_name="%(class)s_created_by", blank=True, null=True)  
	created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True) 
	closed=models.BooleanField(default=False)
	def __str__(self):
		return self.title

class Events(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	title = models.CharField(max_length=250,)
	date = models.DateField()
	time = models.TimeField()
	purpose = models.TextField(blank=True, null=True,)
	notes = models.TextField(blank=True, null=True,)
	venue = models.CharField(max_length=250,blank=True, null=True ,)
	attach_file = models.BinaryField(blank=True, null=True,)
	filename = models.CharField(max_length=250,blank=True, null=True ,)
	file_type = models.CharField(max_length=250,blank=True, null=True ,)
	def __str__(self):
		return self.title

# Projects & Related Entities
class ClientQuery(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
	project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='queries')
	client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='queries')
	notes = models.TextField(null=True,blank=True)
	document = models.BinaryField(null=True,blank=True)
	filename = models.CharField(max_length=255,null=True,blank=True)
	file_type = models.CharField(max_length=100,null=True,blank=True)
	created_by = models.ForeignKey('user_management.User', on_delete=models.SET_NULL, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.project


