from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from requests import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework import status

# Create your views here.
class TemplateListCreateView(APIView):
    def get(self, request):
        records = Template.objects.all()
        serializer = TemplateSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            response_data['id'] = instance.pk
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TemplateRetriveUpdateDestroyView(APIView):
    def get_object(self,pk):
        try:
            return Template.objects.get(pk=pk)
        except Template.DoesNotExist:
            return None
    
    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TemplateSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TemplateDocumentSerializer(records, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
