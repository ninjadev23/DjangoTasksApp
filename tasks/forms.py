from django import forms
from .models import Task
class TaskForm(forms.ModelForm):
	class Meta:
		model = Task
		fields = ["title", "description", "important"]
		widgets = {
			"title":forms.TextInput(attrs={"class":"form-control m-1","placeholder":"Titulo de la tarea"}),
			"description":forms.Textarea(attrs={"class":"form-control m-1","placeholder":"Escribe tu descripcion"}),
			"important":forms.CheckboxInput(attrs={"class":"m-1 form-check-input m-auto",}),
		}
