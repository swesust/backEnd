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


	list_filter = ('is_admin','is_student',)
	list_display = ('userid', 'is_admin', 'is_staff', 'is_student')
	fieldsets = (
		(None,{'fields' : ('userid', 'password','is_student')}),
		('Personal info', {'fields' : ()}),
		('Permission', {'fields' : ('is_admin', 'is_staff', 'groups','user_permissions',)}),
	)

	add_fieldsets = (
		(None, {
			'classes' : ('wide',),
			'fields' : ('userid', 'password1', 'password2', 'is_student')}
			),
	)
	ordering = ('userid',)
	filter_horizontal = ('groups', 'user_permissions',)
	search_fields = ('userid',)


admin.site.register(AuthUser, UserAdmin)
admin.site.register(Batch)
admin.site.register(Student)
admin.site.register(Teacher)