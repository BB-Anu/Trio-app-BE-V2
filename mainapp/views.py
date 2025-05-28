from datetime import timezone
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView, UpdateView, CreateView, DetailView
from django.db.models import Q

from task.models import *
from task.serializers import *
from user_management.models import Role, User
from user_management.serializers import UserSerializer
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
        print('===request.user===',request.user.branch.id)
        # user=User.objects.get(email=request.user)
        # branch_id=user.branch.pk
        # records = ClientProfile.objects.filter(branch=branch_id)
        # user=User.objects.get(roles='auditor')
        # users=User.objects.filter(roles__name='customer')
        # print('---',users)
        records = ClientProfile.objects.filter(branch=request.user.branch.id)
        print('---',records)
        serializer = ClientProfileSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClientProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print('serializer.data',serializer.data)
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Created client profile: {serializer.data.get('business_name', '')}",
        screen_name='client profile',
    )   
            print('log',audit_log)
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
                instance = serializer.instance
                audit_log = AuditLog.objects.create(
                branch = instance.branch ,
                user_id=request.user.pk,
                action=f"Updated client profile: {serializer.data.get('business_name', '')}",
                screen_name='client profile',
            )   
                return Response(serializer.data)
            print('serializer.errors',serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        print(pk)
        print('---------------',request.user.branch.id)
        records = self.get_object(pk)
        if records:
            business_name = records.business_name  
            branch = records.branch  
            records.delete()
            audit_log = AuditLog.objects.create(
            branch=branch,
            user_id=request.user.pk,
            action=f"Deleted client profile: {business_name}",
            screen_name='client profile',
        )
            print('AuditLog',audit_log)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class DocumentGroupListCreateView(APIView):
    def get(self, request):
        records = DocumentGroup.objects.filter(branch=request.user.branch.id)
        serializer = DocumentGroupSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DocumentGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
                branch = instance.branch ,
                user_id=request.user.pk,
                action=f"Created Document",
                screen_name='Document',
            )   
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
                instance = serializer.instance
                audit_log = AuditLog.objects.create(
                branch = instance.branch ,
                user_id=request.user.pk,
                action=f"Updated Document",
                screen_name='Document',
            )   
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            audit_log = AuditLog.objects.create(
                branch = records.branch ,
                user_id=request.user.pk,
                action=f"Deleted Document",
                screen_name='Document',
            )   
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class CustomDocumentEntityListCreateView(APIView):
    def get(self, request):
        records = CustomDocumentEntity.objects.filter(branch=request.user.branch.id)
        serializer = CustomDocumentEntitySerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomDocumentEntitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Created {serializer.data.get('entity_name','')} ",
        screen_name='Custom Document Entity',
    )   
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
                instance = serializer.instance
                audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Updated {serializer.data.get('entity_name','')} ",
        screen_name='Custom Document Entity',
    )   
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            audit_log = AuditLog.objects.create(
            branch=records.branch,
            user_id=request.user.pk,
            action=f"Deleted Custom Entity",
            screen_name='Custom Entity',
        )
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
            print('serializer.data',serializer.data)
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Created Task Template: {serializer.data.get('title', '')}",
        screen_name='Task Template',
    )   
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
                instance = serializer.instance
                audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Updated Task Template: {serializer.data.get('title', '')}",
        screen_name='Task Template',
    )   

                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            audit_log = AuditLog.objects.create(
            branch=records.branch,
            user_id=request.user.pk,
            action=f"Task Teemplate Entity",
            screen_name='Task Template',
        )

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
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Created Trio Group: {serializer.data.get('name', '')}",
        screen_name='Trio Group',
    )   
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
                instance = serializer.instance
                audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Updated Trio Group: {serializer.data.get('name', '')}",
        screen_name='Trio Group',
    )   
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            group=records.name
            records.delete()
            audit_log = AuditLog.objects.create(
            branch=records.branch,
            user_id=request.user.pk,
            action=f"Deleted Trio Group {group}",
            screen_name='Trio Group',
        )

            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class LoanCaseListCreateView(APIView):
    def get(self, request):
        records = LoanCase.objects.filter(branch=request.user.branch.id).exclude(status='approved')
        serializer = LoanCaseSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LoanCaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=instance.created_by.id,
        action=f"Created Loancase: {serializer.data.get('case', '')}",
        screen_name='Loan Case',
    )   
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApprovedLoanCaseListCreateView(APIView):
    def get(self, request):
        records = LoanCase.objects.filter(branch=request.user.branch.id,status='approved')
        serializer = LoanCaseSerializer(records, many=True)
        return Response(serializer.data)

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
                instance = serializer.instance
                audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Updated Loancase: {serializer.data.get('case', '')}",
        screen_name='Loan Case',
    )   
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            case=records.case
            records.delete()
            audit_log = AuditLog.objects.create(
            branch=records.branch,
            user_id=request.user.pk,
            action=f"Deleted Loancase {case}",
            screen_name='Loan Case',
        )


            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
class LoanCaseDetailRetrieveUpdateDestroyView(APIView):
    def get(self, request, pk):
        try:
            case = LoanCase.objects.get(pk=pk)
            print('case',case)
            client=ClientProfile.objects.get(pk=case.client.id)
            print('client',client)
            docs = Document.objects.filter(case=pk)
            assignment = TRIOAssignment.objects.get(case=pk)
            task = Task.objects.filter(assignment=assignment.pk).first()
            if task:
                due_date = task.due_date
                print('---', due_date)   
            else:
                due_date = None         
            timesheet = TaskTimesheet.objects.filter(case=pk)

            return Response({
                'case': LoanCaseSerializer(case).data,
                'assignment': TRIOAssignmentSerializer(assignment).data,
                'docs': DocumentSerializer(docs, many=True).data,
                'client':ClientProfileSerializer(client).data,
                'due_date':due_date,
                'timesheet': TaskTimesheetSerializer(timesheet, many=True).data,
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class ProjectsListCreateView(APIView):
    def get(self, request):
        records = Projects.objects.filter(branch=request.user.branch.id)
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
        records = FolderMaster.objects.filter(branch=request.user.branch.id)
        serializer = FolderMasterSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FolderMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=instance.created_by,
        action=f"Created Folder Master: {serializer.data.get('folder_name', '')}",
        screen_name='Folder Master',
    )   

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
                instance = serializer.instance
                audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Updated Folder Master: {serializer.data.get('folder_name', '')}",
        screen_name='Folder Master',
    )   
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            audit_log = AuditLog.objects.create(
            branch=records.branch,
            user_id=request.user.pk,
            action=f"Deleted Folder <aster",
            screen_name='Folder Master',
        )

            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class TRIOAssignmentListCreateView(APIView):
    def get(self, request):
        records = TRIOAssignment.objects.filter(branch=request.user.branch.id)
        serializer = TRIOAssignmentSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TRIOAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Created Trio Assignment",
        screen_name='Trio Assignment',
    )   
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
                instance = serializer.instance
                audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Updated Trio Assignment",
        screen_name='Trio Assignment',
    )   
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            audit_log = AuditLog.objects.create(
            branch=records.branch,
            user_id=request.user.pk,
            action=f"Deleted TRIO Assignment",
            screen_name='TRIO Assignment',
        )

            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class AuditLogListCreateView(APIView):
    def get(self, request):
        records = AuditLog.objects.filter(branch=request.user.branch.id)
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
        records = ComplianceChecklist.objects.filter(branch=request.user.branch.id)
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
        if request.user.is_superuser:
            records = Document.objects.filter(branch=request.user.branch.id)
            serializer = DocumentSerializer(records, many=True)
            return Response(serializer.data)
        else:
            assignments = TRIOAssignment.objects.filter(assigned_to__id=request.user.id)
            case_ids = assignments.values_list('case__id', flat=True)
            print('assignments',case_ids)
            documents = Document.objects.filter(
                branch=request.user.branch,
                case__id__in=case_ids
            )
            print('records',documents)
            serializer = DocumentSerializer(documents, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance
            user_id=get_object_or_404(ClientProfile,user__user_id=instance.uploaded_by.id)
            user=get_object_or_404(RequestDocument,requested_to=user_id,document_type=instance.document_type)
            user.status="uploaded"
            user.save()
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Created Document",
        screen_name='Document',
            )   
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('-------',serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentApproveListCreateView(APIView):
    def put(self, request, pk):
        try:
            print('====',pk)
            doc = get_object_or_404(Document,pk=pk)
            print('===',doc.id)
            doc.status = 'approved'
            doc.reject_reason=''
            doc.save()
            return Response({'message': 'Document approved successfully.'}, status=status.HTTP_200_OK)
        except Document.DoesNotExist:
            return Response({'error': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DocumentRejectListCreateView(APIView):
    def put(self, request, pk,reject_reason):
        try:
            print('==pk==',pk)
            doc = Document.objects.get(pk=pk)
            print('===',doc.id)
            doc.status = 'returned'
            doc.reject_reason=reject_reason
            doc.save()
            return Response({'message': 'Document approved successfully.'}, status=status.HTTP_200_OK)
        except Document.DoesNotExist:
            return Response({'error': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TimesheetEntryApproveListCreateView(APIView):
    def put(self, request, pk):
        try:
            print('====',pk)
            doc = TimesheetEntry.objects.get(pk=pk)
            print('===',doc)
            doc.status = 'approved'
            doc.approved_by = request.user
            doc.reject_reason=''
            doc.save()
            return Response({'message': 'TimesheetEntry approved successfully.'}, status=status.HTTP_200_OK)
        except TimesheetEntry.DoesNotExist:
            return Response({'error': 'TimesheetEntry not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TimesheetEntryRejectListCreateView(APIView):
    def put(self, request, pk,reject_reason):
        try:
            print('==pk==',pk)
            doc = TimesheetEntry.objects.get(pk=pk)
            print('===',doc)
            doc.status = 'rejected'
            doc.reject_reason=reject_reason
            doc.save()
            return Response({'message': 'TimesheetEntry approved successfully.'}, status=status.HTTP_200_OK)
        except TimesheetEntry.DoesNotExist:
            return Response({'error': 'TimesheetEntry not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TimesheetApproveListCreateView(APIView):
    def put(self, request, pk):
        try:
            doc = TaskTimesheet.objects.get(pk=pk)
            doc.status = 'approved'
            doc.reject_reason = ''
            doc.save()

            try:
                trio = TRIOProfile.objects.get(pk=doc.employee.id)
            except TRIOProfile.DoesNotExist:
                return Response({"error": "TRIO profile not found"}, status=404)

            count = TaskTimesheet.objects.filter(case=doc.case, employee=trio, status='approved').count()
            task_count = TaskTimesheet.objects.filter(case=doc.case, employee=trio).count()

            try:
                task = Task.objects.get(case=doc.case, assigned_to=doc.employee.id)
            except Task.DoesNotExist:
                return Response({"error": "Related task not found"}, status=404)

            task.status = 'completed' if count == task_count else 'in_progress'
            task.save()
            print('case',doc.case.id)
            completed_assignments = Task.objects.filter(case=doc.case, status='pending').count()

            try:
                case_assign = TRIOAssignment.objects.get(case_id=doc.case.id)
                print('case_assign',case_assign)
                case_assign.status = 'completed' if completed_assignments == 0 else 'in_progress'
                case_assign.save()
            except TRIOAssignment.DoesNotExist:
                return Response({"error": "TRIO assignment not found"}, status=404)

            pending_tasks = Task.objects.filter(case=doc.case, status='pending').count()

            try:
                loan_case = LoanCase.objects.get(pk=doc.case.id)
                print('loan_case',loan_case)
                loan_case.status = 'review' if pending_tasks == 0 else 'in_progress'
                loan_case.save()
            except LoanCase.DoesNotExist:
                return Response({"error": "Loan case not found"}, status=404)

            return Response({'message': 'Timesheet approved successfully.'}, status=status.HTTP_200_OK)

        except TaskTimesheet.DoesNotExist:
            return Response({'error': 'Timesheet not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TimesheetRejectListCreateView(APIView):
    def put(self, request, pk,reject_reason):
        try:
            print('==pk==',pk)
            doc = TaskTimesheet.objects.get(pk=pk)
            print('===',doc)
            doc.status = 'rejected'
            doc.reject_reason=reject_reason
            doc.save()
            return Response({'message': 'Timesheet approved successfully.'}, status=status.HTTP_200_OK)
        except Document.DoesNotExist:
            return Response({'error': 'Timesheet not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoanCaseApproveListCreateView(APIView):
    def put(self, request, pk):
        try:
            print('====', pk) 
            doc = LoanCase.objects.get(pk=pk) 
            print('===', doc)

            doc.status = 'approved'  
            doc.reject_reason = ''   
            doc.save()               
            
            client = get_object_or_404(ClientProfile,pk=doc.client)
            client.has_existing_loan=True
            client.save()
            
            assignment = get_object_or_404(TRIOAssignment, case=doc.id)  
            print('assignment', assignment.group)

            group = get_object_or_404(TRIOGroup, pk=assignment.group.id)  
            print('group', group)

            group.is_available = True  
            group.save()              

            return Response({'message': 'LoanCase approved successfully.'}, status=status.HTTP_200_OK)
        except LoanCase.DoesNotExist:
            return Response({'error': 'LoanCase not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoanCaseRejectListCreateView(APIView):
    def put(self, request, pk,reject_reason):
        try:
            print('==pk==',pk)
            doc = LoanCase.objects.get(pk=pk)
            print('===',doc)
            doc.status = 'rejected'
            doc.reject_reason=reject_reason
            doc.save()
            return Response({'message': 'LoanCase approved successfully.'}, status=status.HTTP_200_OK)
        except LoanCase.DoesNotExist:
            return Response({'error': 'LoanCase not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientDocumentListCreateView(APIView):
    def get(self, request,case_id):
        print('---',case_id,request.user.branch.id)
        records = Document.objects.filter(branch=request.user.branch.id,case=case_id)
        print('---',records)
        serializer = DocumentSerializer(records, many=True)
        print(serializer.data)
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
            data = request.data.copy()
            data['status'] = 'pending'
            data['reject_reason'] = ''
            serializer = DocumentSerializer(records, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            audit_log = AuditLog.objects.create(
            branch=records.branch,
            user_id=request.user.pk,
            action=f"Deleted Document",
            screen_name='Document',
        )
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class RiskAssessmentListCreateView(APIView):
    def get(self, request):
        records = RiskAssessment.objects.filter(branch=request.user.branch.id)
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
        records = ClientQuery.objects.filter(branch=request.user.branch.id)
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
        records = TimeSheet.objects.filter(branch=request.user.branch.id)
        serializer = TimeSheetSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TimeSheetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Created  ",
        screen_name='Timehseet',
    )   
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
                instance = serializer.instance
                audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Updated  ",
        screen_name='Timehseet',
    )   
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            audit_log = AuditLog.objects.create(
            branch=records.branch,
            user_id=request.user.pk,
            action=f"Deleted ",
            screen_name='TimeSheet',
        )
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class DocumentUploadListCreateView(APIView):
    def get(self, request):
        records = DocumentUpload.objects.filter(branch=request.user.branch.id)
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
        records = DocumentUploadAudit1.objects.filter(branch=request.user.branch.id)
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
        records = DocumentUploadHistory1.objects.filter(branch=request.user.branch.id)
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
        print('--',request.user)
        records = UserProfile.objects.filter(branch=request.user.branch.id)
        serializer = UserProfileSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Created User profile: {serializer.data.get('user', '')}",
        screen_name='User profile',
    )   
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.data)
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
                instance = serializer.instance
                audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Updated User profile: {serializer.data.get('user', '')}",
        screen_name='User profile',
    )   
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            audit_log = AuditLog.objects.create(
            branch=records.branch,
            user_id=request.user.pk,
            action=f"Deleted ",
            screen_name='UserProfile',
        )
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class DocumentAccessListCreateView(APIView):
    def get(self, request):
        records = DocumentAccess.objects.filter(branch=request.user.branch.id)
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
        records = FileDownloadReason.objects.filter(branch=request.user.branch.id)
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
        records = CaseAssignment.objects.filter(branch=request.user.branch.id)
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
        
        records = TRIOGroupMember.objects.filter(branch=request.user.branch.id)
        serializer = TRIOGroupMemberSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TRIOGroupMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=instance.created_by,
        action=f"Created ",
        screen_name='Trio Group Member',
    )   
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
                instance = serializer.instance
                audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Updated ",
        screen_name='Trio Group Member',
    )   
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            audit_log = AuditLog.objects.create(
            branch=records.branch,
            user_id=request.user.pk,
            action=f"Deleted ",
            screen_name='Trio Group Member',
        )
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class TRIOProfileListCreateView(APIView):
    def get(self, request):
        print(request.data)
        records = TRIOProfile.objects.filter(branch=request.user.branch.id)
        serializer = TRIOProfileSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TRIOProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Created Trio profile: {serializer.data.get('user', '')}",
        screen_name='Trio profile',
    )   
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
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
            print(request.data)
            if serializer.is_valid():
                serializer.save()
                instance = serializer.instance
                audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Updated Trio profile: {serializer.data.get('user', '')}",
        screen_name='Trio profile',
    )   
                return Response(serializer.data)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            audit_log = AuditLog.objects.create(
            branch=records.branch,
            user_id=request.user.pk,
            action=f"Deleted ",
            screen_name='Trio Profile',
        )
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class FinalReportListCreateView(APIView):
    def get(self, request):
        records = FinalReport.objects.filter(branch=request.user.branch.id)
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
        if request.user.is_superuser:
            records = Task.objects.filter(branch=request.user.branch.id)
            serializer = TaskSerializer(records, many=True)
            return Response(serializer.data)    
        else:
            print(request.user)
            user=UserProfile.objects.get(user=request.user.id)
            print('---',user.id)
            profile=TRIOProfile.objects.get(user=user.id)
            print('---',profile.id)

            # assigned_to
            records = Task.objects.filter(branch=request.user.branch.id,assigned_to=profile.id)
            serializer = TaskSerializer(records, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Created Task",
        screen_name='Task',
    )   
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
                instance = serializer.instance
                audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Updated Task",
        screen_name='Task',
    )   
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            audit_log = AuditLog.objects.create(
            branch=records.branch,
            user_id=request.user.pk,
            action=f"Deleted ",
            screen_name='Task',
        )
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class TaskAuditLogListCreateView(APIView):
    def get(self, request):
        records = TaskAuditLog.objects.filter(branch=request.user.branch.id)
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
        records = TaskDeliverable.objects.filter(branch=request.user.branch.id)
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
        if request.user.is_superuser:
            records = TaskTimesheet.objects.filter(branch=request.user.branch.id)
            serializer = TaskTimesheetSerializer(records, many=True)
            return Response(serializer.data)
        else:
            print(request.user.id)
            user=UserProfile.objects.get(user=request.user)
            print('-----user---',user)
            profile=TRIOProfile.objects.get(user=user.id)
            print('-----profile---',profile)

            records = TaskTimesheet.objects.filter(branch=request.user.branch.id,employee=profile.id,status='pending')
            serializer = TaskTimesheetSerializer(records, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = TaskTimesheetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Created Task Timesheet",
        screen_name='Task Timesheet',
    )   
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
                instance = serializer.instance
                audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Updated Task Timesheet",
        screen_name='Task Timesheet',
    )   
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            audit_log = AuditLog.objects.create(
            branch=records.branch,
            user_id=request.user.pk,
            action=f"Deleted ",
            screen_name='Task Timesheet',
        )
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class TaskTimesheetApprovalRetrieveUpdateDestroyView(APIView):
    def get(self, request):
        records = TaskTimesheet.objects.filter(status='completed')
        print('---rec',records)
        serializer = TaskTimesheetSerializer(records, many=True)
        return Response(serializer.data)

class TimesheetEntryApprovalRetrieveUpdateDestroyView(APIView):
    def get(self, request):
        print('--',request.data)
        records = TimesheetEntry.objects.filter(status='completed')
        print('---rec',records)
        serializer = TimesheetEntrySerializer(records, many=True)
        return Response(serializer.data)

class TimesheetEntryListCreateView(APIView):
    def get(self, request):
        records = TimesheetEntry.objects.filter(branch=request.user.branch.id,created_by=request.user)
        serializer = TimesheetEntrySerializer(records, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = TimesheetEntrySerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        timesheet_id = request.data.get('timesheet')
        new_hours = float(request.data.get('hours', 0))
        print('New hours:', new_hours)

        try:
            timesheet = TaskTimesheet.objects.get(id=timesheet_id)
        except TaskTimesheet.DoesNotExist:
            return Response({"error": "Timesheet not found."}, status=status.HTTP_404_NOT_FOUND)

        # Total hours already logged
        total_existing_hours = TimesheetEntry.objects.filter(timesheet=timesheet).aggregate(
            total=models.Sum('hours'))['total'] or 0
        print('Total existing hours:', total_existing_hours)

        remaining_hours = (timesheet.total_working_hours or 0) 

        if new_hours > remaining_hours:
            return Response(
                {"error": f"Only {remaining_hours} working hours are remaining for this timesheet."},
                status=status.HTTP_400_BAD_REQUEST
            )
        remaining_hours-= total_existing_hours
        print('Remaining hours:', remaining_hours)
        # Update total spent hours (optional)
        timesheet.hours_spent +=  new_hours
        timesheet.total_working_hours-=new_hours
        # If fully used, mark completed
        if timesheet.total_working_hours==0:
            timesheet.status = 'completed'
        else:
            timesheet.status = 'pending'

        timesheet.save()

        # Save the entry
        serializer = TimesheetEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user=instance.created_by,
        action=f"Created Timesheet Entry",
        screen_name='Timesheet Entry',
    )   
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

    # def put(self, request, pk):
    #     records = self.get_object(pk)
    #     if records:
    #         serializer = TimesheetEntrySerializer(records, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    def put(self, request, pk):
        instance = self.get_object(pk)
        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND)

        timesheet = instance.timesheet
        new_hours = float(request.data.get('hours', 0))

        total_existing_hours = TimesheetEntry.objects.filter(
            timesheet=timesheet
        ).exclude(id=instance.id).aggregate(total=models.Sum('hours'))['total'] or 0
        remaining_hours = (timesheet.total_working_hours or 0) - total_existing_hours
    
        if new_hours > remaining_hours:
            return Response(
                {"error": f"Only {remaining_hours} working hours are remaining for this timesheet."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TimesheetEntrySerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Update total_working_hours in TimeSheet
            timesheet.total_working_hours = total_existing_hours - new_hours
            timesheet.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            audit_log = AuditLog.objects.create(
            branch=records.branch,
        user=records.updated_by,
            action=f"Deleted ",
            screen_name='Timesheet Entry',
        )
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class TimesheetAttachmentListCreateView(APIView):
    def get(self, request):
        records = TimesheetAttachment.objects.filter(branch=request.user.branch.id)
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
        records = TimesheetDocument.objects.filter(branch=request.user.branch.id)
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
        records = WorkSchedule.objects.filter(branch=request.user.branch.id)
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
        records = TaskExtraHoursRequest.objects.filter(branch=request.user.branch.id)
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
        records = Meetings.objects.filter(branch=request.user.branch.id)
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
        records = AuditorProfile.objects.filter(branch=request.user.branch.id)
        serializer = AuditorProfileSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        serializer = AuditorProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Created Auditor profile: {serializer.data.get('user', '')}",
        screen_name='Auditor profile',
    )   
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
                instance = serializer.instance
                audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Updated Auditor profile: {serializer.data.get('user', '')}",
        screen_name='Auditor profile',
    )   
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            audit_log = AuditLog.objects.create(
            branch=records.branch,
            user_id=request.user.pk,
            action=f"Deleted ",
            screen_name='Auditor Profile',
        )
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class MarketingAgentProfileListCreateView(APIView):
    def get(self, request):
        records = MarketingAgentProfile.objects.filter(branch=request.user.branch.id)
        serializer = MarketingAgentProfileSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MarketingAgentProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Created Agent profile: {serializer.data.get('user', '')}",
        screen_name='Agent profile',
    )   
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
                instance = serializer.instance
                audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Updated Agent profile: {serializer.data.get('user', '')}",
        screen_name='Agent profile',
    )   
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            audit_log = AuditLog.objects.create(
            branch=records.branch,
            user_id=request.user.pk,
            action=f"Deleted ",
            screen_name='Agent',
        )
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class IssueReportListCreateView(APIView):
    def get(self, request):
        records = IssueReport.objects.filter(branch=request.user.branch.id)
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
        records = Notification.objects.filter(branch=request.user.branch.id)
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
        records = LawyerProfile.objects.filter(branch=request.user.branch.id)
        serializer = LawyerProfileSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        serializer = LawyerProfileSerializer(data=request.data)
        print('--',serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Created Lawyer profile: {serializer.data.get('user', '')}",
        screen_name='Lawyer profile',
    )   
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
        print(request.data)
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
                instance = serializer.instance
                audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Updated Lawyer profile: {serializer.data.get('user', '')}",
        screen_name='Lawyer profile',
    )   
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            audit_log = AuditLog.objects.create(
            branch=records.branch,
            user_id=request.user.pk,
            action=f"Deleted ",
            screen_name='Lawyer Profile',
        )
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class MembersListCreateView(APIView):
    def get(self, request):
        records = Members.objects.filter(branch=request.user.branch.id)
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
        records = StaffFeedback.objects.filter(branch=request.user.branch.id)
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
        records = TaskAssignment.objects.filter(branch=request.user.branch.id)
        serializer = TaskAssignmentSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Created ",
        screen_name='Task Assignment',
    )   
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
                instance = serializer.instance
                audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Updated ",
        screen_name='Task Assignment',
    )   
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            audit_log = AuditLog.objects.create(
            branch=records.branch,
            user_id=request.user.pk,
            action=f"Deleted ",
            screen_name='Task Assignment',
        )
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
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Created ",
        screen_name='Template',
    )   
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
                instance = serializer.instance
                audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f"Updated ",
        screen_name='Template',
    )   
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        records = self.get_object(pk)
        if records:
            records.delete()
            audit_log = AuditLog.objects.create(
            branch=records.branch,
            user_id=request.user.pk,
            action=f"Deleted ",
            screen_name='Template',
        )
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)



class TemplateDocumentListCreateView(APIView):
    def get(self, request):
        records = TemplateDocument.objects.filter(branch=request.user.branch.id)
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
            users = UserProfile.objects.filter(
                user__roles__name='Auditor',
                user__branch=request.user.branch,profile_completed=True
            )
            print('---', users)
            serializer = UserProfileSerializer(users, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class ClientUser(APIView):
    def get(self, request):
        try:
            users = UserProfile.objects.filter(
                user__roles__name='customer',
                user__branch=request.user.branch,profile_completed=True
            )                
            print('---',users)
            serializer = UserProfileSerializer(users, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class AgentUser(APIView):
    def get(self, request):
        try:
            users = UserProfile.objects.filter(
                user__roles__name='Marketing Agent',
                user__branch=request.user.branch,profile_completed=True
            )             
            print('---',users)
            serializer = UserProfileSerializer(users, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class LawyerUser(APIView):
    def get(self, request):
        try:
            users = UserProfile.objects.filter(
                user__roles__name='Lawyer',
                user__branch=request.user.branch,profile_completed=True
            )            
            print('---',users)
            serializer = UserProfileSerializer(users, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class TrioUser(APIView):
    def get(self, request):
        try:
            print('---',request.user)
            users = UserProfile.objects.filter(
                ~Q(user__roles__name='customer'),
                branch=request.user.branch.id,profile_completed=True
            )
            print('---',users)
            serializer = UserProfileSerializer(users, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class TrioUserRetrive(APIView):
    def get(self, request,pk):
        try:
            print('---',request.user)
            users = UserProfile.objects.get(pk=pk)            
            print('---',users)
            serializer = UserProfileSerializer(users)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class TrioGroupUser(APIView):
    def get(self, request):
        try:
            print('---',request.user)
            users = UserProfile.objects.filter(
                ~Q(user__roles__name='Customer'),
                branch=request.user.branch.id,profile_completed=True
            )
            print('---',users)
            serializer = UserProfileSerializer(users, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class entities(APIView):
    def get(self, request):
        try:
            users=CustomDocumentEntity.objects.filter(branch=request.user.branch.id)
            serializer = CustomDocumentEntitySerializer(users, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        

class folder(APIView):
    def get(self, request,entityId):
    # Get folders associated with the given entity_id
        try:
            folders = FolderMaster.objects.filter(entity__entity_id=entityId)
            print('---',folders)
            serializer = FolderMasterSerializer(folders, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
                return Response({"error": str(e)}, status=500)
        


class template_task(APIView):
    def get(self, request,pk):
    # Get folders associated with the given entity_id
        try:
            print('---',request.data,pk)
            folders = TaskTimesheet.objects.get(pk=pk)
            print('---',folders)
            serializer = TaskTimesheetSerializer(folders)
            return Response(serializer.data, status=200)
        except Exception as e:
                return Response({"error": str(e)}, status=500)

class Dashboard(APIView):
    def get(self, request):
        try:
            print('--',request.user)
            branch_id = request.user.branch.id
            task_count = Task.objects.filter(branch=branch_id).count()
            assignment_count = TRIOAssignment.objects.filter(branch=branch_id).count()
            triogroup = TRIOGroup.objects.filter(branch=branch_id).count()
            case = LoanCase.objects.filter(branch=branch_id).count()
            recent_tasks = LoanCase.objects.filter(branch=branch_id).order_by('-created_at')[:5]
            serialized_tasks = LoanCaseSerializer(recent_tasks, many=True).data
            assignments = TRIOAssignment.objects.filter(branch=branch_id).order_by('-assigned_on')[:10]
            serialized_assignments = TRIOAssignmentSerializer(assignments, many=True).data
            timesheet=TaskTimesheet.objects.filter(branch=branch_id).count()
            pending_timesheet=TaskTimesheet.objects.filter(branch=branch_id,status='pending').count()
            completed_timesheet=TaskTimesheet.objects.filter(branch=branch_id,status='completed').count()
            approved_timesheet=TaskTimesheet.objects.filter(branch=branch_id,status='approved').count()
            rejected_timesheet=TaskTimesheet.objects.filter(branch=branch_id,status='rejected').count()
            assignment_count = TRIOAssignment.objects.all().count()
            return Response({
                'task': task_count,
                'assignment': assignment_count,
                'group': triogroup,
                'case': case,
                'recent_tasks': serialized_tasks,
                'assignments':serialized_assignments,
                'timesheet':timesheet,
                'pending_timesheet':pending_timesheet,
                'approved_timesheet':approved_timesheet,
                'completed_timesheet':completed_timesheet,
                'rejected_timesheet':rejected_timesheet
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class UserDashboard(APIView):
    def get(self,request):
        try:
            print('---',request.user.id)
            user=TRIOProfile.objects.get(user__user=request.user.id)
            task_count = Task.objects.filter(assigned_to=user).count()
            timesheet=TaskTimesheet.objects.filter(employee=user).count()
            pending_timesheet=TaskTimesheet.objects.filter(employee=user,status='pending').count()
            approved_timesheet=TaskTimesheet.objects.filter(employee=user,status='approved').count()
            rejected_timesheet=TaskTimesheet.objects.filter(employee=user,status='rejected').count()
            tasks=TaskTimesheet.objects.filter(employee=user).order_by('-created_at')[:10]
            recent_task=TaskTimesheetSerializer(tasks,many=True).data
            timesheets=Task.objects.filter(assigned_to=user).order_by('-created_at')[:10]
            recent_timesheets=TaskSerializer(timesheets,many=True).data
            print('--',recent_timesheets)
            return Response({
                'task': task_count,
                'timesheet':timesheet,
                'pending_timesheet':pending_timesheet,
                'approved_timesheet':approved_timesheet,
                'rejected_timesheet':rejected_timesheet,
                'recent_task':recent_task,
                'recent_timesheets':recent_timesheets
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class GetTask(APIView):
    def get(self,request,case_id):
        try:
            print('---',case_id)
            task=Task.objects.get(id=case_id)
            print('task',task.case.id)
            # timesheet=TaskTimesheet.objects.fil(case=task.case.id)
            # print('timesheet',timesheet)
            # case=timesheet.case
            # print('case',case)
            user=UserProfile.objects.get(user=request.user)
            trio=TRIOProfile.objects.get(user=user)
            tasks=TaskTimesheet.objects.filter(case=task.case.id,employee=trio)
            print('tasks',tasks)
            serializer=TaskTimesheetSerializer(tasks,many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
        
class TimesheetsReport(APIView):
    def get(self, request, date=None):
        try:
            status_param = request.GET.get('status')  # Optional status filter
            print('--- Date:', date, 'Status:', status_param)
            if date:
                timesheets = TaskTimesheet.objects.filter(created_at=date)
            if status_param and date:
                timesheets = TaskTimesheet.objects.filter(created_at=date,status=status_param)
            else:
                timesheets = TaskTimesheet.objects.filter(created_at=timezone.now().date())


            print('-- Filtered Timesheets:', timesheets)
            serializer = TaskTimesheetSerializer(timesheets, many=True)
            return Response(serializer.data, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        


class CaseReport(APIView):
    def get(self, request, date=None):
        try:
            print('--', date)
            if date:
                date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            else:
                date_obj = timezone.now().date()

            loancase = LoanCase.objects.filter(created_at__date=date_obj)

            print('-- Filtered:', loancase)
            serializer = LoanCaseSerializer(loancase, many=True)
            return Response(serializer.data, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

class CaseDocument(APIView):
   def get(self, request):
    try:
        print('---', request.user.id)

        # Get assignments for this user
        assignments = TRIOAssignment.objects.filter(assigned_to=request.user.id)
        print('assignments', assignments)

        # Get all related case IDs from assignments
        case_ids = assignments.values_list('case_id', flat=True)
        print('case_ids', list(case_ids))

        # Fetch the LoanCases using the case_ids
        records = LoanCase.objects.filter(id__in=case_ids)
        print('records', records)

        # Serialize the data
        serializer = LoanCaseSerializer(records, many=True)
        print('serializer', serializer.data)

        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


class TimeSheetEntryView(APIView):
    def get(self,request,pk):
        try:
        # timesheet=TaskTimesheet.objects.get(pk=pk)
            entry=TimesheetEntry.objects.filter(timesheet=pk)
            serializer=TimesheetEntrySerializer(entry,many=True).data
            return Response(serializer,status=200)
        
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class TimeSheetEntryView1(APIView):
    def get(self,request,pk):
        try:
        # timesheet=TaskTimesheet.objects.get(pk=pk)
            entry=TimesheetEntry.objects.get(pk=pk)
            serializer=TimesheetEntrySerializer(entry).data
            return Response(serializer,status=200)
        
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class customer_Screen(APIView):
    def get(self,request,pk):
        try:
            print('pp',pk)
            user_info=UserProfile.objects.get(user=pk)
            print('--',user_info)
            client_profile=ClientProfile.objects.get(user=user_info.id)
            print('---',client_profile)
            case_details=LoanCase.objects.get(client=client_profile.id)
            print('--',case_details)
            return Response({
                    'case': LoanCaseSerializer(case_details).data,
                    'user': UserProfileSerializer(user_info).data,
                    'client':ClientProfileSerializer(client_profile).data,
                })        
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class RequestDocumentListCreateView(APIView):
    def get(self, request):
        print(request.data)
        if request.user.is_superuser:
            records = RequestDocument.objects.filter(branch=request.user.branch.id)
            serializer =  RequestDocumentSerializer(records, many=True)
            return Response(serializer.data)
        else:
            records =  RequestDocument.objects.filter(branch=request.user.branch.id)
            serializer =  RequestDocumentSerializer(records, many=True)
            return Response(serializer.data)

    def post(self, request):
        print('request',request.data)
        data = request.data.copy() 
        user_id = data.get('requested_to')
        client_profile = get_object_or_404(ClientProfile, user__user_id=user_id)
        data['requested_to'] = client_profile.id
        print('----data',data)
        serializer = RequestDocumentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance
            audit_log = AuditLog.objects.create(
        branch = instance.branch ,
        user_id=request.user.pk,
        action=f" Requested Document",
        screen_name=' RequestDocument',
        )   
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('-------',serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestedDocumentListCreateView(APIView):
    def get(self, request):
        try:
            if request.user.is_superuser:
                records = RequestDocument.objects.filter(branch=request.user.branch.id)
                print('records',records)
                serializer = RequestDocumentSerializer(records,many=True)
                print('serializer',serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:

                print('request',request.user.id)
                client_profile = get_object_or_404(ClientProfile, user__user_id=request.user.id)
                records = RequestDocument.objects.filter(branch=request.user.branch.id, requested_to=client_profile)
                print('records',records)
                serializer = RequestDocumentSerializer(records,many=True)
                print('serializer',serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except RequestDocument.DoesNotExist:
            return Response({'detail': 'Requested document not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print('Error occurred:', str(e))
            return Response({'detail': 'An unexpected error occurred.'}, status=status.HTTP_400_BAD_REQUEST)
        




class TRIORequestedDocumentListCreateView(APIView):
    def get(self, request):
        try:
            if request.user.is_superuser:
                records = RequestDocument.objects.filter(branch=request.user.branch.id)
                print('records',records)
                serializer = RequestDocumentSerializer(records,many=True)
                print('serializer',serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                records = RequestDocument.objects.filter(branch=request.user.branch.id, requested_by=request.user.id)
                print('records',records)
                serializer = RequestDocumentSerializer(records,many=True)
                print('serializer',serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except RequestDocument.DoesNotExist:
            return Response({'detail': 'Requested document not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print('Error occurred:', str(e))
            return Response({'detail': 'An unexpected error occurred.'}, status=status.HTTP_400_BAD_REQUEST)


class TRIOGroupMemberListRetrieveUpdateDestroyView(APIView):
    def get(self, request, pk):
        try:
            print('-- Group ID:', pk)
            group_members = TRIOGroupMember.objects.get(group=pk)
            trio_assignment=TRIOAssignment.objects.get(group=pk)
            print('assignment',trio_assignment.case.id)
            # Prepare data structure
            trio_data = []

            # Iterate over the ManyToMany profiles
            for user_profile in group_members.profile.all():
                print('user_prof', user_profile)
                try:
                    # Get TRIOProfile for this user_profile
                    trio = TRIOProfile.objects.get(user=user_profile)
                    print('--- TRIO Profile:', trio)

                    # Get tasks for this TRIOProfile
                    member_tasks = TaskTimesheet.objects.filter(employee=trio,case=trio_assignment.case.id)
                    print(f'--- Tasks for {trio.id}:', member_tasks)
                    completed_tasks = TaskTimesheet.objects.filter(case=trio_assignment.case.id,status='completed')
                    print(f'---completed_tasks  for {trio.id}:', completed_tasks)

                    pending_tasks = TaskTimesheet.objects.filter(case=trio_assignment.case.id,status='pending')
                    print(f'--- pending_tasks for {trio.id}:', pending_tasks,pending_tasks.count())

                    rejected_tasks = TaskTimesheet.objects.filter(case=trio_assignment.case.id,status='rejected')
                    print(f'--- rejected_tasks for {trio.id}:', rejected_tasks)

                    approved_tasks = TaskTimesheet.objects.filter(case=trio_assignment.case.id,status='approved')
                    print(f'--- approved_tasks for {trio.id}:', approved_tasks)

                    # Serialize the tasks
                    tasks_serializer = TaskTimesheetSerializer(member_tasks, many=True)
                    completed_tasks_serializer = TaskTimesheetSerializer(completed_tasks, many=True)
                    pending_tasks_serializer = TaskTimesheetSerializer(pending_tasks, many=True)
                    rejected_tasks_serializer = TaskTimesheetSerializer(rejected_tasks, many=True)
                    approved_tasks_serializer = TaskTimesheetSerializer(approved_tasks, many=True)

                    # Append to result
                    trio_data.append({
                        "trio_profile_id": trio.id,
                        "user_profile_id": user_profile.id,
                        "user_full_name": str(user_profile.user.first_name),  
                        "tasks": tasks_serializer.data,
                        "completed_tasks":completed_tasks_serializer.data,
                        "pending_tasks":pending_tasks_serializer.data,
                        "rejected_tasks":rejected_tasks_serializer.data,
                        "approved_tasks":approved_tasks_serializer.data,
                    })

                except TRIOProfile.DoesNotExist:
                    print(f'--- No TRIOProfile found for user_profile {user_profile}')
                    continue

            serializer = TRIOGroupMemberSerializer(group_members)         
            print(f'completed_tasks_count: {sum(len(member["completed_tasks"]) for member in trio_data)}')
            total_pending= pending_tasks.count()

            return Response({
                "group_member": serializer.data,
                "members_with_tasks": trio_data,
                "task_count": sum(len(member["tasks"]) for member in trio_data),
                "completed_tasks_count": completed_tasks.count(),
                "total_pending": total_pending,
                "rejected_tasks_count": rejected_tasks.count(),
                "approved_tasks_count": approved_tasks.count(),
            }, status=status.HTTP_200_OK)

        except TRIOGroupMember.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
