from django import forms
from .models import *
import sys
from django.core.exceptions import ValidationError

class RegistrationForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=30, widget=forms.TextInput())
    last_name = forms.CharField(label='Last Name', max_length=30, widget=forms.TextInput())
    dob = forms.DateField(label='Date of Birth', widget = forms.TextInput(attrs={"class":"datepicker"}))
    image = forms.ImageField()
    class_id = forms.ChoiceField(label='Class')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password (Again)',widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['class_id'].choices = [(class_obj.id,class_obj.name) for class_obj in Class.objects.all()]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self._errors['password2'] = self.error_class(['Password mismatched'])
        
        return self.cleaned_data.get('password2')
    
    def clean_email(self):
        if Student.objects.filter(email=self.cleaned_data.get("email")).exists():
            self._errors['email'] = self.error_class(['Email exists already!'])
        return self.cleaned_data.get("email")

class StudentForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=30, widget=forms.TextInput())
    last_name = forms.CharField(label='Last Name', max_length=30, widget=forms.TextInput())
    dob = forms.DateField(label='Date of Birth', widget = forms.TextInput(attrs={"class":"datepicker"}))
    image = forms.ImageField()
    email = forms.EmailField(label='Email')
    class_field = forms.ChoiceField(label='Class')

    def __init__(self,student_id, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['class_field'].choices = [(class_obj.id,class_obj.name) for class_obj in Class.objects.all()]
        student = Student.objects.get(id=student_id)
        self.fields['first_name'].initial = student.first_name
        self.fields['last_name'].initial = student.last_name
        self.fields['dob'].initial = student.dob
        self.fields['image'].initial = student.image
        self.fields['email'].initial = student.email

    def clean_class_field(self):
        return Class.objects.get(id=self.cleaned_data.get('class_field'))