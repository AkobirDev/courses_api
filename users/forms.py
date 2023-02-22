from django import forms

from users.models import CustomUser

class RegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email',
                   'avatar', 'bio', 'phone_number', 'is_teacher', 'password')
        
    def save(self, commit=False):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'avatar') 