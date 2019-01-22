from django.db import models
from . import helper
from django.utils.timezone import now
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager,PermissionsMixin, 
	_user_has_module_perms, _user_has_perm, _user_get_all_permissions)

from django.contrib.auth import get_backends


class Batch(models.Model):
	"""
	contain the Batch information
	Parameters:

		`name`: batch name 
		`year`: batch year
	"""
	name = models.CharField(max_length=100)
	year = models.CharField(max_length=4, unique=True)

	# default: object output
	def __str__(self):
		return self.name+ " - " + self.year

class UserManager(BaseUserManager):

	"""
	UserManager stands for creating new AuthUser.
	For custom authentication model there must need a custom manager.
	`create_user` and `create_superuser` are the abstract methods of the
	`BaseUserManager`. `create_staffuser` is an extended method of the 
	`BaseUserManager`.
	"""

	def create_user(self,userid,password=None,name=None,email=None,
		is_staff=False,is_admin=False, is_student=True):
		if not password:
			raise ValueError('password needed')
		if not name:
			raise ValueError('name needed')
		if not email:
			raise ValueError('email needed')

		user = self.model(userid=userid)
		user.name = name
		user.email = email
		user.is_admin = is_admin
		user.is_staff = is_staff
		user.is_student = is_student
		user.set_password(password)
		user.save(self._db)
		return user

	def create_staffuser(self, userid, password, name, email, is_student):
		"""
		to create custom permission level user
		"""
		if not userid or password:
			raise ValueError('must have the userid and password')
		if not name:
			raise ValueError('name needed')
		if not email:
			raise ValueError('email needed')


		user = self.create_user(userid, password, name, email, True,False,is_student)
		return user

	def create_superuser(self, userid, password, name, email, is_student):
		"""
		to create an admin
		"""
		if not userid or not password:
			raise ValueError('must have userid and password')
		if not name:
			raise ValueError('name needed')
		if not email:
			raise ValueError('email needed')


		user = self.create_user(userid, password, name, email, True, True, is_student)
		return user

class AuthUser(AbstractBaseUser,PermissionsMixin):
	
	"""
	Custom user model for authentication.
	
	Parameters:
		`userid`: User unique id for user authentication. 
				  Students - Reg ID
				  Teachers - User Name

		`name` : User Display name

		`email` : User email account 

		`is_active`: Identify whether the user is currently using the site or not. This is
					 an extended variable from `AbstractBaseUser`
		`is_student`: Identify the user is a student or a teacher. This is a flag variable
		              decalered for differentiate the user.

		`is_admin`: Identify the user is an admin or not. This is an extended value from
					`AbstractBaseUser`
		`is_staff`: Identify the user to providing access in the admin panel with limited permissions.
					This is an extended variable from `AbstractBaseUser`
		`object`: Instance of the UserManager to connect with the database. 


		`USERNAME_FIELD`: must be defined for custom authentication model to identify the username field.
		`REQUIRED_FIELDS`: list of required fields to create a new user. 

		Extended methods for permission level checking
			`has_perm(...)`
			`has_perms(...)`
			`has_module_perms(...)`
			`username(self)`


	"""
	userid = models.CharField(max_length=120, unique=True)
	is_active = models.BooleanField(default=True)
	is_student = models.BooleanField(default=True)

	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	
	# user display Name
	name = models.CharField(max_length=80)
	# user email
	email = models.EmailField(max_length=120, default='swe@student.sust.edu',unique=True)

	objects = UserManager()

	USERNAME_FIELD = 'userid'
	REQUIRED_FIELDS = ['name','email','is_student',]


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

class Student(models.Model):
	"""
	Student profile model to store a particular student information
	Informations:
		* Registration ID : 2016831035
		* Batch : Foreign-Key-> Batch Object
		* Phone : 01********
		* Address : Brahmanbaria
		* Birthday : 15th March ****
		* Alumni: True(student graduated) | False(studying)
		* Blood Group : B+
		* Gender : M (Male)
		* Display Image : storagelocation:(data/student/2016/2016831035/image.png)
		* Github Profile : rafiulgits (https://github.com/rafiulgits)
		* Linkedin Profile : rafiul15 (https://linkedin.com/in/rafiul15)

	Student extra informations will saved as JSON: 
		data/students/2016/2016831035/contents.json 
		
		prototype:
		{
			'bio' : 'This is user bio',
			'works' ['working as a programmer in X', 'worked as a program tester in Y'],
			'skill': ['android', 'django'],
			'programming language' : ['C', 'Java', 'Python'],
			'interested': ['programming', 'developing', 'leadership'],
			'projects': ['github.com/rafiulgits/IP-Messenger', 'github.com/sakkhat/Project250'],
			'codefores': account id
			.
			.
			.
		}

		`see`: swe.helper.Conntent for more informations
	"""

	# Connect with user authentication model
	user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
	# Student Reg ID
	regid = models.CharField(max_length=10, unique=True, primary_key=True, editable=True)
	# Connect with batch model
	batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
	# Student Phone number
	phone = models.CharField(max_length=16, default = '880') 
	# Student address
	address = models.CharField(max_length=30,default = 'Sylhet')
	# Student birthday
	birthday = models.DateField(default=now)
	# If student graduated then True or False
	alumni = models.BooleanField(default=False)
	# Student blood group
	BLOOD_GROUPS = (
		('A+', 'A+'),
		('A-', 'A-'),
		('B+', 'B+'),
		('B-', 'B-'),
		('O+', 'O-'),
		('O-', 'O-'),
		('AB+', 'AB+'),
		('AB-', 'AB-')
		)
	bloodgroup = models.CharField(max_length=3, choices=BLOOD_GROUPS)
	# {M:Male} {F:Female} {T:Third Gender}
	GENDER_CHOICE = (
		('M', 'Male'),
		('F', 'Female'),
		('T', 'Third Gender'))
	gender = models.CharField(max_length=1, choices=GENDER_CHOICE, default='F')
	# Profile Image location
	imgsrc = models.CharField(max_length=100,default = 'data/image.PNG')
	# Github : rafiulgits
	githubid = models.CharField(max_length=20,default = 'home')
	# Linkedin : rafiul15
	linkedinid = models.CharField(max_length=30,default = 'home')
	# Facebook : ******
	facebookid = models.CharField(max_length=30, default='home')
	# twitter : rafiultweets
	twitterid = models.CharField(max_length=20, default='home')

	# default: object output
	def __str__(self):
		return self.regid

class Teacher(models.Model):
	"""
	Teacher profile model to store a particular teacher information.
	Information:
		Position: Job position
		Alumni: True | False
		Phone: +000000
		Leaved: Indicate that the teacher is continuing or not
		Head: Indicate the dept. head 
		Gender: M(Male) | F(Female) | T(Third Gender)
		Image: Storage location (data/teachers/userid/image.JPG)

	
		Extra informations will similary saved in a JSON file. 
			data/teachers/userid/contents.json

			prototype:
			{
				'reseach' : ['natural langauage processing', 'AI'],
			}

	"""
	user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)

	JOB_POSITIONS = (
		('Lecturer', 'Lecturer'),
		('Assistant Professor', 'Assistant Professor'),
		('Associate Professor', 'Associate Professor'),
		('Professor', 'Professor'))

	position = models.CharField(max_length=25, choices=JOB_POSITIONS)
	alumni = models.BooleanField(default=False)
	phone = models.CharField(max_length=16,default = '880')
	leaved = models.BooleanField(default=False)
	head = models.BooleanField(default=False)

	GENDER_CHOICE = (
		('M', 'Male'),
		('F', 'Female'),
		('T', 'Third Gender'))
	gender = models.CharField(max_length=1, choices=GENDER_CHOICE, default='F')
	imgsrc = models.CharField(max_length=100,default = 'data/image.PNG')
	
	# default: object output
	def __str__(self):
		return self.user.name

class Post(models.Model):
	"""
	Feed post model. 
	
	Parameters:
		`title`: Post title
		`body`: Post body
		`time`: Post created time
		`user`: User who create a post
		`has_media`: Indicate that the post has any image or not
		`imgsrc`: Post image storage link
	"""
	# title can be bengali, so make max_length little bit larger
	title = models.CharField(max_length=150)
	# body can be a large text	
	body = models.TextField()
	# auto generate date and time 
	# TODO: timezone problem
	time_date = models.DateTimeField(auto_now_add=True)
	# link the post created user
	user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
	# if the post carry an image then this will be `True`
	has_media = models.BooleanField(default=False)
	# image location: posts/currentmillisec.type
	imgsrc = models.CharField(max_length=50, default='none')



# TODO
# class Endrosements(models.Model):
# 	key = models.CharField()
# 	value = models.TextField()
# 	user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)


# class Working(models.Model):
# 	company = models.CharField(max_length=40)
# 	position = models.CharField(max_length = 25)
# 	from_date = models.DateField()
# 	current = models.BooleanField(default=False)
# 	to_date = models.DateField()