from django import forms
from .models import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body', 'tags']

        labels = {
        	'body': _('Describe your problem'),
        }
        help_texts = {
            'title': _('Don\'t be shy - ask a question'),
            'body': _('Those who can help may need some more information'),
            'tags': _('Choose a tag to help people find your question'),
        }
        error_messages = {
            'title': {
                'max_length': _("This field is way too long!"),
            },
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'How to fall asleep with opened eyes?'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows':'5'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class SignUpForm(forms.ModelForm):
	username = forms.CharField(label='Username',
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'BeastMaster64'}))
	email = forms.CharField(label='Email',
		widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.ru'}))
	password1 = forms.CharField(label='Password',
		widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	password2 = forms.CharField(label='Repeat password',
		widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	class Meta:
		model = Profile
		fields = ['username', 'email', 'password1', 'password2', 'avatar', 'date']

		labels = {
        	# 'email': _('Email'),
        	'avatar': _('Upload avatar'),
        	'date': _('Date of birth')
        }

		widgets = {
			'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
			'date': forms.DateInput(attrs={'class': 'form-control'}),
		}

	def clean(self):
		if not self.cleaned_data['password1'] == self.cleaned_data['password2']:
			raise forms.ValidationError(
				_("Passwords don't match!"),
				code='different_passwords')
		if User.objects.filter(username__iexact=self.cleaned_data['username']).exists():
			raise forms.ValidationError(
				_("This username is already taken"),
				code='username_taken',)
		return self.cleaned_data


class LoginForm(AuthenticationForm):
	def confirm_login_allowed(self, user):
		if not user.is_active:
			raise forms.ValidationError(
				_("This account is inactive."),
				code='inactive')
	username = forms.CharField(label='Username',
		widget=forms.TextInput(attrs={'class': 'form-control form_centered',
									'placeholder': 'Username',
									'autofocus':''}))
	password = forms.CharField(label='Password',
		widget=forms.PasswordInput(attrs={'class': 'form-control form_centered',
									'placeholder': 'Password'}))
