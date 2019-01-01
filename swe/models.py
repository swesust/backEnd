from django.db import models
from . import helper
from hashlib import sha1

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
	name = models.CharField(max_length=80)
	regid = models.CharField(max_length=10)
	#batch: 2016, 2017;
	batch = models.CharField(max_length=4)
	email = models.CharField(max_length=100)
	phone = models.CharField(max_length=16)
	address = models.CharField(max_length=30)
	#blood group: AB+, O-, O+, B+
	bloodgroup = models.CharField(max_length=3)
	#gender: F = female; M = male
	gender = models.CharField(max_length=1)
	# static storage location : data/students/batch/regid/image.png 
	imgsrc = models.CharField(max_length=100)
	# githubid : rafiulgits
	githubid = models.CharField(max_length=20)
	# linkedin : rafiul15
	linkedinid = models.CharField(max_length=30)
	# contents json file location: data/students/batch/regid/content.json
	contentloc = models.CharField(max_length=70)

	# default: object output
	def __str__(self):
		return "\nName: {}\nRegID: {}".format(self.name, self.regid)




class Batch(models.Model):
	"""
		Contains the batch list
		Attributes:
		* Batch Name : The Initial(Prarombik) 
		* Year : 2016
	"""
	name = models.CharField(max_length=50)
	year = models.CharField(max_length=4)

	# default: object output
	def __str__(self):
		return "\nName: {}\nYear: {}".format(self.name, self.year)




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
	name = models.CharField(max_length=80)
	# hash id for teacher
	hid = models.CharField(max_length = 9)
	email = models.CharField(max_length=100)
	position = models.CharField(max_length=20)
	phone = models.CharField(max_length=16)
	gender = models.CharField(max_length=1)
	# static storage location : data/teachers/hid/image.png
	imgsrc = models.CharField(max_length=100)
	# content json file location: data/teachers/hid/content.json
	contentloc = models.CharField(max_length=70)

	#
	# default: object output
	def __str__(self):
		return "\nName: {}".format(self.name)

	def makehid(self):
		# 8 length hash code
		self.hid = str(int(sha1(str(self.id).encode()).hexdigest(),16)%(10**8))



#####################################################################
# new model for student and teacher authentications
# used sha256 hashing to encode passwords
		
class StudentLog(models.Model):
	"""
		Contains students authentication informations: Reg ID and Password
	"""
	regid = models.CharField(max_length=10)
	# sha256 hash need 64 character
	password = models.CharField(max_length=65)
	# 32 characters random hash
	randhash = models.CharField(max_length=40)

	# default: object output
	def __str__(self):
		return "\nID: {}".format(self.regid)



class TeacherLog(models.Model):
	"""
		Contains teachers authentications informations : Email and Password
	"""
	email = models.CharField(max_length=100)
	# sha256 hash need 64 characters 
	password = models.CharField(max_length=65)
	# 32 characters random hash
	hashrand = models.CharField(max_length=40)

	# default: object output
	def __str__(self):
		return "\nEmail: {}".format(self.email)

