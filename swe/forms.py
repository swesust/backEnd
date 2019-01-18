from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()

"""
	django custom user model form 
	`see`: https://github.com/django/django/blob/master/django/contrib/auth/forms.py
"""

class RegisterForm(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('userid','is_student',)

	def clean_userid(self):
		"""	
		to check the user is already taken or not
		"""
		userid = self.cleaned_data.get('userid')
		query = User.objects.filter(userid=userid)

		if query.exists():
			raise forms.ValidationError('User id taken')

		return userid

	def clean_password2(self):
		"""
		checking two raw passwords and return the password if matched
		"""
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Password don't matched")
		return password2
	

class UserAdminCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('userid','is_student',)

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Password don't matched")
		return password2

	def save(self, commit=True):
		user = super(UserAdminCreationForm,self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user


class UserAdminChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ('is_admin', 'is_staff', 'is_student',)


	def clean_password(self):
		return self.initial["password"]


class LoginForm(forms.Form):
	userid = forms.CharField(max_length=120,
		widget=forms.TextInput(attrs={
			'placeholder': 'User ID',
			'class' : 'regno-input full-width'}))

	password = forms.CharField(
		widget=forms.PasswordInput(attrs={
			'placeholder' : 'Password',
			'class' : 'pass-input full-width'}))


class UserRecognize(forms.Form):
	userid = forms.CharField(max_length=120, widget=forms.TextInput(attrs={
		'placeholder' : 'User ID'}))

class UserToken(forms.Form):
	token = forms.CharField(max_length=155, widget=forms.TextInput(attrs={
		'placeholder' : 'Your Token'}))