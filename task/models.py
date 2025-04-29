from django.db import models

# Create your models here.
from ckeditor.fields import RichTextField

class Template(models.Model):
    name = models.CharField(max_length=100)
    content =models.CharField(max_length=500)

    def __str__(self):
        return self.name
    
class TemplateDocument(models.Model):
    Template=models.ForeignKey(Template,related_name='template',on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()  # Adjust as per your needs, e.g., RichTextField from CKEditor
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document created at {self.created_at}"
    
