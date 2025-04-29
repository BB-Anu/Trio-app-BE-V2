from rest_framework import serializers
from .models import *

class TemplateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Template
		fields = "__all__"

class TemplateDocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = TemplateDocument
		fields = "__all__"

