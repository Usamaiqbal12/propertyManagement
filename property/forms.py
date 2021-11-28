from django import forms
from django.forms import widgets
from django.forms.models import modelformset_factory
from .models import Property, PropertyUser


class PropertyForm(forms.ModelForm):
    error_css_class = 'error-field'
    
    class Meta:
        model = Property
        fields = ['block','plot_num', 'area', 'is_alloted', 'files']

    block = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}))
    plot_num = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}))
    area = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}))
    is_alloted = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control form-check-input'}))
    files = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control form-control-sm'}))




class PropertyUserForm(forms.ModelForm):
    class Meta:
        model = PropertyUser
        fields = ['full_name','phone']
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        # django-crispy-forms
            for field in self.fields:
                new_data = {
                    "placeholder": f'Property {str(field)}',
                    "class": 'form-control',
                }
                self.fields[str(field)].widget.attrs.update(
                    new_data
                )
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-2'}))        
                
PropertyUserFormset = modelformset_factory(PropertyUser, form=PropertyUserForm, extra=0)
property_update_formset = modelformset_factory(PropertyUser, form=PropertyUserForm, extra=0, can_delete=True)