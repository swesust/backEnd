from django.db import models
from . import helper
from django.utils.timezone import now
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager,PermissionsMixin, 
	_user_has_module_perms, _user_has_perm, _user_get_all_permissions)

from django.contrib.auth import get_backends


class Batch(models.Model):
	"""
		Contains the batch list
		Attributes:
		* Batch Name : The Initial(Prarombik) 
		* Year : 2016
	"""
	name = models.CharField(max_length=100)
	year = models.CharField(max_length=4, unique=True)

	# default: object output
	def __str__(self):
		return self.name+ "|" + self.year

class UserManager(BaseUserManager):

	def create_user(self, userid, password=None, is_staff=False, is_admin=False):
		if not userid:
			raise ValueError('must have reg id')
		
		user = self.model(userid = userid)
		user.is_staff = is_staff
		user.is_admin = is_admin
		user.set_password(password)
		user.save(self._db)
		return user

	def create_staffuser(self, userid, password):
		if not userid or password:
			raise ValueError('must have the userid and password')

		user = self.model(userid, password,True,False)
		return user

	def create_superuser(self, userid, password):

		if not userid or not password:
			raise ValueError('must have userid and password')

		user = self.create_user(userid, password, True, True)
		return user

class AuthUser(AbstractBaseUser,PermissionsMixin):
	
	userid = models.CharField(max_length=120, unique=True)
	is_active = models.BooleanField(default=True)

	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	
	objects = UserManager()

	USERNAME_FIELD = 'userid'
	REQUIRED_FIELDS = []


	def has_perm(self, perm, obj=None):
		pass

	def has_perms(self, perm_list, obj=None):
		pass

	def has_module_perms(self, app_label):
		if self.is_admin or self.is_staff:
			return True
		return False

	def has_perm(self, perm, obj=None):
		if self.is_admin:
			return True
		return _user_has_perm(self, perm, obj)

	def has_perms(self, perm_list, obj=None):
		return all(self.has_perm(perm, obj) for perm in perm_list)

	def has_module_perms(self, app_label):
		if self.is_admin or self.is_staff:
			return True
		return False

	def get_username(self):
		return self.userid
		
	def __str__(self):
		return self.userid

class Student(models.Model):
	"""
	Student model contains all the basic informations about a student
	Informations:
		* Name : Rafiul Islam
		* Registration ID : 2016831035
		* Batch : 2016 
		* Email : mohammad35@student.sust.edu
		* Phone : 01********
		* Address : Akhaura, Brahmanbaria
		* Birthday : 15th March 1998
		* Blood Group : B+
		* Gender : M (Male)
		* Display Image : storagelocation:Image
		* Github Profile : https://github.com/rafiulgits
		* Linkedin Profile : https://linkedin.com/in/rafiul15

		CV contents will saved in a JSON file:
		{
			'knowing' : ['C', 'Java'],
			'interested' : ['Cyber Security']
		}
	"""
	user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, default='')
	name = models.CharField(max_length=80, default = '')
	regid = models.CharField(max_length=10)
	#batch: 2016, 2017;
	batch = models.ForeignKey(Batch, on_delete=models.CASCADE, default = '')
	email = models.EmailField(max_length=120, default = '')
	phone = models.CharField(max_length=16, default = '') 
	address = models.CharField(max_length=30,default = '')
	# date of birth: 01011900 = 01 Jan 1900
	birthday = models.DateField(default=now)
	#blood group: AB+, O-, O+, B+
	bloodgroup = models.CharField(max_length=3,default = '')
	#gender: F = female; M = male
	gender = models.CharField(max_length=1,default = '')
	# static storage location : data/students/batch/regid/image.png 
	imgsrc = models.CharField(max_length=100,default = '')
	# githubid : rafiulgits
	githubid = models.CharField(max_length=20,default = '')
	# linkedin : rafiul15
	linkedinid = models.CharField(max_length=30,default = '')

	# default: object output

	def __str__(self):
		return self.name

class Teacher(models.Model):
	"""
		Contains teachers informations
		Attributes:
		* Name : Asif Mohammad Samir
		* Email : ****@gmail.com
		* Position : Assistant Professor
		* Phone : 01*********
		* Gender : M (Male)
		* Display Image : storagelocation:Image

		Teachers contents:
		a json file
	"""
	user = models.ForeignKey(AuthUser, on_delete=models.CASCADE,default='')
	name = models.CharField(max_length=80,default = '')
	# TODO: 100001 starting id
	hid = models.CharField(max_length = 5, default = '')
	email = models.EmailField(max_length=120, default = '')
	position = models.CharField(max_length=30,default = '')
	phone = models.CharField(max_length=16,default = '')
	gender = models.CharField(max_length=1,default = '')
	# static storage location : data/teachers/hid/image.png
	imgsrc = models.CharField(max_length=100,default = '')
	
		
	# default: object output
	def __str__(self):
		return self.name


