from django import forms

class SubscriptionForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True,
        label='Enter your Email Address to Subscribe', label_suffix="!")
