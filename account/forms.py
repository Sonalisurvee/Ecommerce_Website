from django import forms
from .models import Address

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "phone", "pincode", "state", "city", "house_name"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form","placeholder":"Full Name"}
        )
        self.fields["phone"].widget.attrs.update(
            {"class": "form-control mb-2 account-form","pattern":"[0-9]{10}","placeholder":"Phone"}
        )
        self.fields["pincode"].widget.attrs.update(
            {"class": "form-control mb-2 account-form","placeholder":"Pincode"}
        )
        self.fields["state"].widget.attrs.update(
            {"class": "form-control mb-2 account-form","placeholder":"Your State"}
        )
        self.fields["city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form","placeholder":" Your City"}
        )
        self.fields["house_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form","placeholder":"House name"}
        )