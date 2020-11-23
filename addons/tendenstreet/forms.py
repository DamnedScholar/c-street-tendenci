from django import forms

class SubscriptionForm(forms.Form):
    email = forms.EmailField(label='Please enter your email address', max_length=100)
