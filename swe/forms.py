from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()



class RegisterForm(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('userid',)

	def clean_userid(self):
		userid = self.cleaned_data.get('userid')
		query = User.objects.filter(userid=userid)

		if query.exists():
			raise forms.ValidationError('User id taken')

		return userid

	def clean_password2(self):
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
		fields = ('userid',)

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
		fields = ('is_admin', 'is_staff')


	def clean_password(self):
		return self.initial["password"]