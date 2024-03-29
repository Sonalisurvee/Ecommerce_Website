from django import forms
from django.core.validators import RegexValidator
from .models import Address

class UserAddressForm(forms.ModelForm):
    phone_validator = RegexValidator(
    regex=r'^[1-9][0-9]{9}$',
    message='Phone number must be 10 digits and not start with 0'
    )
    pincode_validator = RegexValidator(
    regex=r'^[1-9]\d{5}$',
    message='Pincode must be 6 digits and should not start with 0'
    )
    name_validator = RegexValidator(
        regex=r'^[a-zA-Z ]+$',
        message='Name must contain only letters'
    )


    class Meta:
        model = Address
        fields = ["full_name", "phone", "pincode", "state", "city", "house_name"]
        error_messages = {
            'full_name': {'required': 'Please enter your full name'},
            'phone': {'required': 'Please enter your phone number'},
            'pincode': {'required': 'Please enter your pincode'},
            'state': {'required': 'Please enter your state'},
            'city': {'required': 'Please enter your city'},
            'house_name': {'required': 'Please enter your house name'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form","placeholder":"Full Name"}
        )
        self.fields["full_name"].required = True
        self.fields["full_name"].validators = [self.name_validator]

        self.fields["phone"].widget.attrs.update(
            {"class": "form-control mb-2 account-form","placeholder":"0987654321"}
        )        
        self.fields["phone"].validators = [self.phone_validator]
        self.fields["phone"].required = True   

        self.fields["pincode"].widget.attrs.update(
            {"class": "form-control mb-2 account-form","placeholder":"Pincode"}
        )
        self.fields["pincode"].validators = [self.pincode_validator]
        self.fields["pincode"].required = True   
        
        self.fields["state"].widget.attrs.update(
            {"class": "form-control mb-2 account-form","placeholder":"Your State"}
        )
        self.fields["state"].required = True 
        self.fields["state"].validators = [self.name_validator]

        self.fields["city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form","placeholder":" Your City"}
        )
        self.fields["city"].required = True
        self.fields["city"].validators = [self.name_validator]


        self.fields["house_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form","placeholder":"House name"}
        )
        self.fields["house_name"].required = True
        self.fields["house_name"].validators = [self.name_validator]


