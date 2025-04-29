from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView, UpdateView, CreateView, DetailView

from task.models import *
from task.serializers import *
from user_management.models import Role, User
from .models import *
from .api_call import call_post_method_without_token_app_builder,call_get_method,call_get_method_without_token,call_post_with_method,call_post_method_for_without_token,call_delete_method,call_delete_method_without_token, call_put_method,call_put_method_without_token
import requests
import json
from django.contrib import messages
from django.urls import resolve, reverse
import jwt
from django.contrib.auth import logout
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from django.contrib import messages

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from django.contrib import messages
from django.conf import settings

BASE_URL = 'http://127.0.0.1:2222/'
APP_BUILDER = 'http://127.0.0.1:8000/'

def dashboard(request):
    return render(request, 'dashboard.html')

class SetupView(APIView):
    def get(self, request):
        records = UserTypeMaster.objects.all()
        serializer = UserTypeMasterSerializer(records, many=True)
        return Response(serializer.data)
    def post(self, request):   
        serializer =  request.data # DATA STURCTURE Come like [{},{}]
        for data in serializer: 
            if data == "usertype":
                for data1 in request.data["usertype"]:
                    serializer = UserTypeMasterSerializer(data = data1)
                    if serializer.is_valid():
                        print("usertype data saved")
                        serializer.save()
                    else:
                        print("error",serializer.errors)
            elif data == "screentable":
                for data1 in request.data["screentable"]:
                    serializer = ScreenSerializer(data = data1)
                    if serializer.is_valid():
                        print("screen data saved")
                        serializer.save()
                    else:
                        print("error",serializer.errors)
            elif data == "screenversion":
                for data1 in request.data["screenversion"]:
                    serializer = ScreenVersionSerializer(data = data1)
                    if serializer.is_valid():
                        print("screen version data saved")
                        serializer.save()
        else:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class ClientProfileListCreateView(APIView):
    # permission_classes = [IsAuthenticated] 
    def get(self, request):
        print('===request.user===',request.user)
        # user=User.objects.get(email=request.user)
        # branch_id=user.branch.pk
        # records = ClientProfile.objects.filter(branch=branch_id)
        # user=User.objects.get(roles='auditor')
        records = ClientProfile.objects.all()
        serializer = ClientProfileSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClientProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientProfileRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated] 
    def get_object(self, pk):
        try:
            return ClientProfile.objects.get(pk=pk)
        except ClientProfile.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = ClientProfileSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = ClientProfileSerializer(records, data=request.data)
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

class DocumentGroupListCreateView(APIView):
    def get(self, request):
        records = DocumentGroup.objects.all()
        serializer = DocumentGroupSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DocumentGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentGroupRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return DocumentGroup.objects.get(pk=pk)
        except DocumentGroup.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = DocumentGroupSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = DocumentGroupSerializer(records, data=request.data)
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

class CustomDocumentEntityListCreateView(APIView):
    def get(self, request):
        records = CustomDocumentEntity.objects.all()
        serializer = CustomDocumentEntitySerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomDocumentEntitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomDocumentEntityRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return CustomDocumentEntity.objects.get(pk=pk)
        except CustomDocumentEntity.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = CustomDocumentEntitySerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = CustomDocumentEntitySerializer(records, data=request.data)
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

class TaskTemplateListCreateView(APIView):
    def get(self, request):
        records = TaskTemplate.objects.all()
        serializer = TaskTemplateSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        print('data',request.data)
        placeholders = request.data.get('placeholders', {})
        print('---palcy',placeholders)
        # values = list(placeholders.values())
        # print('---values',values)
        complete_data = {
                **placeholders,
                'branch': request.data.get('branch'),
                'template': request.data.get('template')
            }
        serializer = TaskTemplateSerializer(data=complete_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskTemplateRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return TaskTemplate.objects.get(pk=pk)
        except TaskTemplate.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TaskTemplateSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TaskTemplateSerializer(records, data=request.data)
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

class TRIOGroupListCreateView(APIView):
    def get(self, request):
        print('===request.user===',request.user)
        user=User.objects.get(email=request.user)
        branch_id=user.branch.pk
        records = TRIOGroup.objects.filter(branch=branch_id)
        serializer = TRIOGroupSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TRIOGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TRIOGroupRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return TRIOGroup.objects.get(pk=pk)
        except TRIOGroup.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TRIOGroupSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TRIOGroupSerializer(records, data=request.data)
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

class LoanCaseListCreateView(APIView):
    def get(self, request):
        records = LoanCase.objects.all()
        serializer = LoanCaseSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LoanCaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoanCaseRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return LoanCase.objects.get(pk=pk)
        except LoanCase.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = LoanCaseSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = LoanCaseSerializer(records, data=request.data)
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

class ProjectsListCreateView(APIView):
    def get(self, request):
        records = Projects.objects.all()
        serializer = ProjectsSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectsRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Projects.objects.get(pk=pk)
        except Projects.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = ProjectsSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = ProjectsSerializer(records, data=request.data)
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

class DocumentTypeListCreateView(APIView):
    def get(self, request):
        records = DocumentType.objects.all()
        serializer = DocumentTypeSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DocumentTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentTypeRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return DocumentType.objects.get(pk=pk)
        except DocumentType.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = DocumentTypeSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = DocumentTypeSerializer(records, data=request.data)
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

class FolderMasterListCreateView(APIView):
    def get(self, request):
        records = FolderMaster.objects.all()
        serializer = FolderMasterSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FolderMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FolderMasterRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return FolderMaster.objects.get(pk=pk)
        except FolderMaster.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = FolderMasterSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = FolderMasterSerializer(records, data=request.data)
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

class TRIOAssignmentListCreateView(APIView):
    def get(self, request):
        records = TRIOAssignment.objects.all()
        serializer = TRIOAssignmentSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TRIOAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TRIOAssignmentRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return TRIOAssignment.objects.get(pk=pk)
        except TRIOAssignment.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TRIOAssignmentSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TRIOAssignmentSerializer(records, data=request.data)
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

class AuditLogListCreateView(APIView):
    def get(self, request):
        records = AuditLog.objects.all()
        serializer = AuditLogSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AuditLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuditLogRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return AuditLog.objects.get(pk=pk)
        except AuditLog.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = AuditLogSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = AuditLogSerializer(records, data=request.data)
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

class ComplianceChecklistListCreateView(APIView):
    def get(self, request):
        records = ComplianceChecklist.objects.all()
        serializer = ComplianceChecklistSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ComplianceChecklistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComplianceChecklistRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return ComplianceChecklist.objects.get(pk=pk)
        except ComplianceChecklist.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = ComplianceChecklistSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = ComplianceChecklistSerializer(records, data=request.data)
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

class DocumentListCreateView(APIView):
    def get(self, request):
        records = Document.objects.all()
        serializer = DocumentSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('-------',serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = DocumentSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = DocumentSerializer(records, data=request.data)
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

class RiskAssessmentListCreateView(APIView):
    def get(self, request):
        records = RiskAssessment.objects.all()
        serializer = RiskAssessmentSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        print('request',request.data)
        serializer = RiskAssessmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RiskAssessmentRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return RiskAssessment.objects.get(pk=pk)
        except RiskAssessment.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = RiskAssessmentSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = RiskAssessmentSerializer(records, data=request.data)
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

class ClientQueryListCreateView(APIView):
    def get(self, request):
        records = ClientQuery.objects.all()
        serializer = ClientQuerySerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClientQuerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientQueryRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return ClientQuery.objects.get(pk=pk)
        except ClientQuery.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = ClientQuerySerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = ClientQuerySerializer(records, data=request.data)
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

class TimeSheetListCreateView(APIView):
    def get(self, request):
        records = TimeSheet.objects.all()
        serializer = TimeSheetSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TimeSheetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('serializer.errors',serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimeSheetRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return TimeSheet.objects.get(pk=pk)
        except TimeSheet.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TimeSheetSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TimeSheetSerializer(records, data=request.data)
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

class DocumentUploadListCreateView(APIView):
    def get(self, request):
        records = DocumentUpload.objects.all()
        serializer = DocumentUploadSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DocumentUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('-------',serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentUploadRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return DocumentUpload.objects.get(pk=pk)
        except DocumentUpload.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = DocumentUploadSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = DocumentUploadSerializer(records, data=request.data)
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

class DocumentUploadAudit1ListCreateView(APIView):
    def get(self, request):
        records = DocumentUploadAudit1.objects.all()
        serializer = DocumentUploadAudit1Serializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DocumentUploadAudit1Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentUploadAudit1RetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return DocumentUploadAudit1.objects.get(pk=pk)
        except DocumentUploadAudit1.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = DocumentUploadAudit1Serializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = DocumentUploadAudit1Serializer(records, data=request.data)
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

class DocumentUploadHistory1ListCreateView(APIView):
    def get(self, request):
        records = DocumentUploadHistory1.objects.all()
        serializer = DocumentUploadHistory1Serializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DocumentUploadHistory1Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('serializer.errors',serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentUploadHistory1RetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return DocumentUploadHistory1.objects.get(pk=pk)
        except DocumentUploadHistory1.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = DocumentUploadHistory1Serializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = DocumentUploadHistory1Serializer(records, data=request.data)
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

class UserProfileListCreateView(APIView):
    def get(self, request):
        records = UserProfile.objects.all()
        serializer = UserProfileSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = UserProfileSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = UserProfileSerializer(records, data=request.data)
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


class DocumentAccessListCreateView(APIView):
    def get(self, request):
        records = DocumentAccess.objects.all()
        serializer = DocumentAccessSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DocumentAccessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('serializer.errors',serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentAccessRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return DocumentAccess.objects.get(pk=pk)
        except DocumentAccess.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = DocumentAccessSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = DocumentAccessSerializer(records, data=request.data)
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

class FileDownloadReasonListCreateView(APIView):
    def get(self, request):
        records = FileDownloadReason.objects.all()
        serializer = FileDownloadReasonSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FileDownloadReasonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('serializer.errors',serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileDownloadReasonRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return FileDownloadReason.objects.get(pk=pk)
        except FileDownloadReason.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = FileDownloadReasonSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = FileDownloadReasonSerializer(records, data=request.data)
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

class CaseAssignmentListCreateView(APIView):
    def get(self, request):
        records = CaseAssignment.objects.all()
        serializer = CaseAssignmentSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CaseAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CaseAssignmentRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return CaseAssignment.objects.get(pk=pk)
        except CaseAssignment.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = CaseAssignmentSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = CaseAssignmentSerializer(records, data=request.data)
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

class TRIOGroupMemberListCreateView(APIView):
    def get(self, request):
        
        records = TRIOGroupMember.objects.all()
        serializer = TRIOGroupMemberSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TRIOGroupMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TRIOGroupMemberRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return TRIOGroupMember.objects.get(pk=pk)
        except TRIOGroupMember.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TRIOGroupMemberSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TRIOGroupMemberSerializer(records, data=request.data)
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

class TRIOProfileListCreateView(APIView):
    def get(self, request):
        records = TRIOProfile.objects.all()
        serializer = TRIOProfileSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TRIOProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TRIOProfileRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return TRIOProfile.objects.get(pk=pk)
        except TRIOProfile.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TRIOProfileSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TRIOProfileSerializer(records, data=request.data)
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

class FinalReportListCreateView(APIView):
    def get(self, request):
        records = FinalReport.objects.all()
        serializer = FinalReportSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FinalReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FinalReportRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return FinalReport.objects.get(pk=pk)
        except FinalReport.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = FinalReportSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = FinalReportSerializer(records, data=request.data)
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

class TaskListCreateView(APIView):
    def get(self, request):
        records = Task.objects.all()
        serializer = TaskSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TaskSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TaskSerializer(records, data=request.data)
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

class TaskAuditLogListCreateView(APIView):
    def get(self, request):
        records = TaskAuditLog.objects.all()
        serializer = TaskAuditLogSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskAuditLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskAuditLogRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return TaskAuditLog.objects.get(pk=pk)
        except TaskAuditLog.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TaskAuditLogSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TaskAuditLogSerializer(records, data=request.data)
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

class TaskDeliverableListCreateView(APIView):
    def get(self, request):
        records = TaskDeliverable.objects.all()
        serializer = TaskDeliverableSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskDeliverableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('serializer.errors',serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDeliverableRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return TaskDeliverable.objects.get(pk=pk)
        except TaskDeliverable.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TaskDeliverableSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TaskDeliverableSerializer(records, data=request.data)
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

class TaskTimesheetListCreateView(APIView):
    def get(self, request):
        records = TaskTimesheet.objects.all()
        serializer = TaskTimesheetSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskTimesheetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskTimesheetRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return TaskTimesheet.objects.get(pk=pk)
        except TaskTimesheet.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TaskTimesheetSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TaskTimesheetSerializer(records, data=request.data)
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

class TimesheetEntryListCreateView(APIView):
    def get(self, request):
        records = TimesheetEntry.objects.all()
        serializer = TimesheetEntrySerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TimesheetEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimesheetEntryRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return TimesheetEntry.objects.get(pk=pk)
        except TimesheetEntry.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TimesheetEntrySerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TimesheetEntrySerializer(records, data=request.data)
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

class TimesheetAttachmentListCreateView(APIView):
    def get(self, request):
        records = TimesheetAttachment.objects.all()
        serializer = TimesheetAttachmentSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TimesheetAttachmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimesheetAttachmentRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return TimesheetAttachment.objects.get(pk=pk)
        except TimesheetAttachment.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TimesheetAttachmentSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TimesheetAttachmentSerializer(records, data=request.data)
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

class TimesheetDocumentListCreateView(APIView):
    def get(self, request):
        records = TimesheetDocument.objects.all()
        serializer = TimesheetDocumentSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TimesheetDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimesheetDocumentRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return TimesheetDocument.objects.get(pk=pk)
        except TimesheetDocument.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TimesheetDocumentSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TimesheetDocumentSerializer(records, data=request.data)
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

class WorkScheduleListCreateView(APIView):
    def get(self, request):
        records = WorkSchedule.objects.all()
        serializer = WorkScheduleSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WorkScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WorkScheduleRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return WorkSchedule.objects.get(pk=pk)
        except WorkSchedule.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = WorkScheduleSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = WorkScheduleSerializer(records, data=request.data)
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

class TaskExtraHoursRequestListCreateView(APIView):
    def get(self, request):
        records = TaskExtraHoursRequest.objects.all()
        serializer = TaskExtraHoursRequestSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskExtraHoursRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskExtraHoursRequestRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return TaskExtraHoursRequest.objects.get(pk=pk)
        except TaskExtraHoursRequest.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TaskExtraHoursRequestSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TaskExtraHoursRequestSerializer(records, data=request.data)
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

class MeetingsListCreateView(APIView):
    def get(self, request):
        records = Meetings.objects.all()
        serializer = MeetingsSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MeetingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeetingsRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Meetings.objects.get(pk=pk)
        except Meetings.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = MeetingsSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = MeetingsSerializer(records, data=request.data)
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

class AuditorProfileListCreateView(APIView):
    def get(self, request):
        records = AuditorProfile.objects.all()
        serializer = AuditorProfileSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AuditorProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuditorProfileRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return AuditorProfile.objects.get(pk=pk)
        except AuditorProfile.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = AuditorProfileSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = AuditorProfileSerializer(records, data=request.data)
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

class MarketingAgentProfileListCreateView(APIView):
    def get(self, request):
        records = MarketingAgentProfile.objects.all()
        serializer = MarketingAgentProfileSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MarketingAgentProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MarketingAgentProfileRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return MarketingAgentProfile.objects.get(pk=pk)
        except MarketingAgentProfile.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = MarketingAgentProfileSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = MarketingAgentProfileSerializer(records, data=request.data)
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

class IssueReportListCreateView(APIView):
    def get(self, request):
        records = IssueReport.objects.all()
        serializer = IssueReportSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IssueReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IssueReportRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return IssueReport.objects.get(pk=pk)
        except IssueReport.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = IssueReportSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = IssueReportSerializer(records, data=request.data)
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

class NotificationListCreateView(APIView):
    def get(self, request):
        records = Notification.objects.all()
        serializer = NotificationSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Notification.objects.get(pk=pk)
        except Notification.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = NotificationSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = NotificationSerializer(records, data=request.data)
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

class LawyerProfileListCreateView(APIView):
    def get(self, request):
        records = LawyerProfile.objects.all()
        serializer = LawyerProfileSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LawyerProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LawyerProfileRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return LawyerProfile.objects.get(pk=pk)
        except LawyerProfile.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = LawyerProfileSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = LawyerProfileSerializer(records, data=request.data)
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

class MembersListCreateView(APIView):
    def get(self, request):
        records = Members.objects.all()
        serializer = MembersSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MembersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MembersRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Members.objects.get(pk=pk)
        except Members.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = MembersSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = MembersSerializer(records, data=request.data)
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

class EventsListCreateView(APIView):
    def get(self, request):
        print('===request.user===',request.user)
        user=User.objects.get(email=request.user)
        branch_id=user.branch.pk
        records = Events.objects.filter(branch=branch_id)
        serializer = EventsSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        print('===request.user===',request.data)
        serializer = EventsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventsRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Events.objects.get(pk=pk)
        except Events.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = EventsSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = EventsSerializer(records, data=request.data)
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

class StaffFeedbackListCreateView(APIView):
    def get(self, request):
        records = StaffFeedback.objects.all()
        serializer = StaffFeedbackSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StaffFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StaffFeedbackRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return StaffFeedback.objects.get(pk=pk)
        except StaffFeedback.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = StaffFeedbackSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = StaffFeedbackSerializer(records, data=request.data)
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

class TaskAssignmentListCreateView(APIView):
    def get(self, request):
        records = TaskAssignment.objects.all()
        serializer = TaskAssignmentSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskAssignmentRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return TaskAssignment.objects.get(pk=pk)
        except TaskAssignment.DoesNotExist:
            return None

    def get(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TaskAssignmentSerializer(records)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        records = self.get_object(pk)
        if records:
            serializer = TaskAssignmentSerializer(records, data=request.data)
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


class TemplateListCreateView(APIView):
    def get(self, request):
        records = Template.objects.all()
        serializer = TemplateSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
            serializer = TemplateSerializer(records, data=request.data)
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



class TemplateDocumentListCreateView(APIView):
    def get(self, request):
        records = TemplateDocument.objects.all()
        serializer = TemplateDocumentSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        # data = request.POST.copy()
        # data['content'] = content   
        print(request.data)    
        serializer = TemplateDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  
class TemplateDocumentRetriveUpdateDestroyView(APIView):
    def get_object(self,pk):
        try:
            return TemplateDocument.objects.get(id=pk)
        except TemplateDocument.DoesNotExist:
            return None
    
    def get(self, request, id):
        records = self.get_object(id)
        if records:
            serializer = TemplateDocumentSerializer(records)
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
    
class AuditorUser(APIView):
    def get(self, request):
        try:
            role = Role.objects.get(name='auditor')
            users = User.objects.filter(roles=role)
            records = AuditorProfile.objects.filter(user__in=users)
            serializer = AuditorProfileSerializer(records, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
