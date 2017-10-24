from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ChangeEmail(forms.Form):
    email = forms.EmailField(label=u'Type new email', required=False)
    email_confirm = forms.EmailField(label=u'Type email again', required=False)


'''class UserChangeForm(UserChangeForm):
    email = forms.EmailField(required=True)
    password = forms.PasswordInput()
    class Meta:
        model = User
        fields = ('password', 'email',)
        exclude = ('username', 'first_name', 'last_name',)

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        if commit:
            user.save()
        return user
'''