from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from .models import *
from .forms import UserAdminCreationForm, UserAdminChangeForm

class UserAdmin(BaseUserAdmin):
	"""
	extended django Admin Interface
	`see`: https://github.com/django/django/blob/master/django/contrib/auth/admin.py
	"""

	form = UserAdminChangeForm
	add_form = UserAdminCreationForm


	list_filter = ('is_admin','is_student','email')
	list_display = ('userid','name', 'is_admin', 'is_staff', 'is_student')
	fieldsets = (
		(None,{'fields' : ('userid', 'password','is_student')}),
		('Personal info', {'fields' : ('name', 'email',)}),
		('Permission', {'fields' : ('is_admin', 'is_staff', 'groups','user_permissions',)}),
	)

	add_fieldsets = (
		(None, {
			'classes' : ('wide',),
			'fields' : ('userid','name', 'email', 'password1', 'password2', 'is_student')}
			),
	)
	ordering = ('userid',)
	filter_horizontal = ('groups', 'user_permissions',)
	search_fields = ('userid',)


class ProfileAdminModel(admin.ModelAdmin):
	"""
	extended class of Model admin.
	This class is stand for added custom search field in admin panel for student profile
	with student reg id
	"""
	search_fields = ('regid',)

admin.site.register(AuthUser, UserAdmin)
admin.site.register(Batch)
admin.site.register(Student, ProfileAdminModel)
admin.site.register(Teacher)
admin.site.register(Post)
admin.site.register(Endrosement)
admin.site.register(Working)