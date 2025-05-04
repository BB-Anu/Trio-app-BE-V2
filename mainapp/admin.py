from django.contrib import admin
from .models import *

admin.site.register(UserTypeMaster)
admin.site.register(Events)
admin.site.register(TaskAssignment)
admin.site.register(TaskTemplate)
admin.site.register(ClientProfile)
admin.site.register(TRIOProfile)
admin.site.register(UserProfile)
admin.site.register(DocumentUpload)
admin.site.register(LoanCase)
admin.site.register(TaskTimesheet)