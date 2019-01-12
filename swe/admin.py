from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from .models import *
from .forms import UserAdminCreationForm, UserAdminChangeForm

class UserAdmin(BaseUserAdmin):
	form = UserAdminChangeForm
	add_form = UserAdminCreationForm


	list_filter = ('is_admin',)
	list_display = ('userid', 'is_admin', 'is_staff')
	fieldsets = (
		(None,{'fields' : ('userid', 'password')}),
		('Personal info', {'fields' : ()}),
		('Permission', {'fields' : ('is_admin', 'is_staff', 'groups','user_permissions',)}),
	)

	add_fieldsets = (
		(None, {
			'classes' : ('wide',),
			'fields' : ('userid', 'password1', 'password2')}
			),
	)
	ordering = ('userid',)
	filter_horizontal = ('groups', 'user_permissions',)
	search_fields = ('userid',)


admin.site.register(AuthUser, UserAdmin)
admin.site.register(Batch)
admin.site.register(Student)
admin.site.register(Teacher)