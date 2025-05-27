from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    contact_number = models.PositiveBigIntegerField()
    email = models.EmailField(unique=True)
    # country = models.ForeignKey('County', on_delete=models.CASCADE, related_name='%(class)s_countries',blank=True,null=True)
    # subcountry =models.ForeignKey('SubCounty', on_delete=models.CASCADE, related_name='%(class)s_sub_countries',blank=True,null=True)    
    company_logo = models.FileField(upload_to='user profile/', null=True, blank=True)
    local_currency = models.CharField(max_length=100,blank=True, null=True)
    incorporation_number = models.CharField()
    website = models.URLField(blank=True, null=True)
    incorporation_number = models.CharField(max_length=100)
    number_of_branches = models.IntegerField()
    number_of_staffs = models.IntegerField()
    end_of_financial_year = models.DateField(blank=True,null=True)
    end_of_month_date = models.DateField(blank=True,null=True)
    amount_rounded_to = models.IntegerField()
    company_api_id = models.CharField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("User", on_delete=models.CASCADE, related_name="company_created_by",
                                   blank=True, null=True)
    update_by = models.ForeignKey("User", on_delete=models.CASCADE, related_name="company_update_by",
                                  blank=True, null=True)
    def __str__(self):
        return self.name


class Branch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.PositiveBigIntegerField()
    manager_name = models.CharField(max_length=100)
    # country = models.ForeignKey('County', on_delete=models.CASCADE, related_name='countries',blank=True,null=True)
    # subcountry =models.ForeignKey('SubCounty', on_delete=models.CASCADE, related_name='sub_countries',blank=True,null=True)
    local_currency = models.CharField(max_length=100,blank=False, null=False)
    description = models.TextField()
    branch_api_id = models.CharField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("User", on_delete=models.CASCADE, related_name="branch_created_by",
                                   blank=True, null=True)
    update_by = models.ForeignKey("User", on_delete=models.CASCADE, related_name="branch_update_by",
                                blank=True, null=True)


    def __str__(self):
        return f"{self.name} - {self.company.name}"

class Function(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    function_name = models.CharField(max_length=250,)
    function_id = models.CharField(max_length=250,blank=True, null=True ,)
    description = models.TextField(blank=True, null=True,)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE,blank=True, null=True,related_name="Function_created_by")
    created_at = models.DateTimeField(auto_now=True)
    update_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True,related_name="Function_update_by")
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.function_name

class Role(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=250,blank=True, null=True ,)
    description = models.TextField(blank=True, null=True,)
    permissions = models.ManyToManyField(Function,related_name='roles',null=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE,blank=True, null=True,related_name="role_created_by")
    created_at = models.DateTimeField(auto_now=True)
    update_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True,related_name="role_update_by")
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("checker", True)
        return self.create_user(email, password, **other_fields)
        
    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError(("You must provide a valid email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user
	
class User(AbstractBaseUser, PermissionsMixin):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    dob=models.DateField(null=True,blank=True)
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    )
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES, null=True, blank=True)
    profile_image = models.ImageField(upload_to='user profile/', null=True, blank=True)
    email = models.EmailField(("email address"), unique=True)
    phone_number = models.IntegerField(null=True, blank=True)
    password=models.CharField(max_length=100, blank=False, null=False)
    roles = models.ForeignKey('user_management.Role', on_delete=models.CASCADE, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    maker = models.BooleanField(default=False)
    checker = models.BooleanField(default=False)
    objects = CustomUserManager()
    REQUIRED_FIELDS = ["first_name"]
    USERNAME_FIELD = "email"
    def __str__(self) -> str:
        return self.email
    
class County(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=250,)
    created_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE,related_name='%(class)s_county_created_by', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True,blank=True, null=True,)
    updated_by =models.ForeignKey('user_management.User', on_delete=models.CASCADE,related_name='%(class)s_county_updated_by', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True, null=True,)
    def __str__(self):
        return self.name

class SubCounty(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=250,)
    county = models.ForeignKey('user_management.County', on_delete=models.CASCADE,related_name='%(class)s_county', blank=True, null=True)
    created_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE,related_name='%(class)s_subcounty_created_by', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True,blank=True, null=True,)
    updated_by =models.ForeignKey('user_management.User', on_delete=models.CASCADE,related_name='%(class)s_subcounty_updated_by', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True, null=True,)
    def __str__(self):
        return self.name

class Ward(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=250,)
    subcounty = models.ForeignKey('user_management.SubCounty', on_delete=models.CASCADE,related_name='%(class)s_sub_county', blank=True, null=True)
    created_by = models.ForeignKey('user_management.User', on_delete=models.CASCADE,related_name='%(class)s_ward_created', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True,blank=True, null=True,)
    updated_by =models.ForeignKey('user_management.User', on_delete=models.CASCADE,related_name='%(class)s_ward_updated', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True, null=True,)
    def __str__(self):
        return self.name