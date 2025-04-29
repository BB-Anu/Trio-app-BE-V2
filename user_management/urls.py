from django.urls import path
from .views import *
urlpatterns = [	
    path("company/", CompanyListCreateView.as_view(), name="company-create"),
	path("company/<pk>/", CompanyRetrieveUpdateDestroyView.as_view(), name="company-update"),
	path("select_company/", SelectCompanyListCreateView.as_view(), name="select-company"),
	path("get_company/", GetCompanyListCreateView.as_view(), name="get-company"),

	path("branch/", BranchListCreateView.as_view(), name="branch-create"),
	path("branch/<pk>/",  BranchRetrieveUpdateDestroyView.as_view(), name="branch-update"),
	path("select_branch/<pk>/", SelectBranchListCreateView.as_view(), name="branch-select"),

    path("function/", FunctionListCreateView.as_view(), name="function-create"),
	path("function/<pk>/", FunctionRetrieveUpdateDestroyView.as_view(), name="function-update"),

	path("county/", CountyListCreateView.as_view(), name="county-create"),
	path("county/<pk>/", CountyRetrieveUpdateDestroyView.as_view(), name="county-update"),

	path("role/", RoleListCreateView.as_view(), name="role-create"),
	path("role/<pk>/", RoleRetrieveUpdateDestroyView.as_view(), name="role-update"),

	path("subcounty/", SubCountyListCreateView.as_view(), name="subcounty-create"),
	path("subcounty/<pk>/", SubCountyRetrieveUpdateDestroyView.as_view(), name="subcounty-update"),

	path("ward/", WardListCreateView.as_view(), name="ward-create"),
	path("ward/<pk>/", WardRetrieveUpdateDestroyView.as_view(), name="ward-update"),

	path("user/", UserListCreateView.as_view(), name="user-create"),	
    path("user_update/", UserUpdateCreateView.as_view(), name="user-update"),
	path("user/<pk>/", UserRetrieveUpdateDestroyView.as_view(), name="user-update"),

	path("function_setup/", RoleRetrieveUpdateDestroyView.as_view(), name="function-setup"),
    path('api/user/', get_logged_in_user, name='get_logged_in_user'),

	path('api_functions_setup/', FunctionSetupAPI.as_view(), name='function-setup'),
	path('function_all/', FunctionAllAPI.as_view(), name='function-all'),
	
	path('permission/<int:role_id>/', GetUserPermissionAPI.as_view(), name='permission'),
	path('user_permission/<int:user_id>/', GetPermissionAPI.as_view(), name='user_permission'),
	path('role_permission/<int:pk>/', GetRolePermissionAPI.as_view(), name='role_permission'),

]

