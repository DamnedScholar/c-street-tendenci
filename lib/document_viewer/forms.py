from django import forms

class SubscriptionForm(forms.Form):
    email = forms.EmailField(
        max_length=100, required=True,
        label='Enter your Email Address',
        widget=forms.EmailInput({
            'class': 'h-12 first:rounded-l-full last:rounded-r-full',
            'data-subscription-target': 'input'
        })
    )
