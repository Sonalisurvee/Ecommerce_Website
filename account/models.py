from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User


# Create your models here.

class  MyAccountManager(BaseUserManager):
    # to create a normal user
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')
        user =self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),#normalize will convert the email into small letters 
        )
        # the things inside the user model are the things mentioned in the create_user function

        user.set_password(password) #will set the password
        user.save(using=self._db)
        return user
    
    # create a super user
    def create_superuser(self,first_name,last_name,username,email,password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),#normalize will convert the email into small letters
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user




# this id the account model
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50,default='ANy')
    last_name = models.CharField(max_length=50,default='Name')
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=50)

    #required fields
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    # default false means a user has no administrative privileges, if True then we give administrative access to a user.
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    # WE are setting email as our login custom way instead of the username
    REQUIRED_FIELDS = ['username', 'first_name','last_name']

    # here in accounts we need to say to accounts that we are performing some fun in MyAccountManger so that acoount will userderstand 
    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    # manditory functions
    def has_perm(self,perm,obj=None):
        return self.is_admin
    # this fun means that is the user is the admin then he has the right to make the changes

    def has_module_perms(self,add_label):
        return True
    




class UserOTP(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    otp_received_time = models.DateTimeField(auto_now_add=True)
    otp = models.IntegerField()