from django.urls import path
from .views import *
urlpatterns = [
    path('templates/', TemplateListCreateView.as_view(), name='templates-create'),
    path('templates/<int:pk>/', TemplateRetriveUpdateDestroyView.as_view(), name='template-update'),
]