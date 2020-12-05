from django import forms

class SubscriptionForm(forms.Form):
    email = forms.EmailField(label='Enter your Email Address to Subscribe', max_length=100, label_suffix="!")
