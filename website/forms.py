from django import forms

from website.models import ContactInquiry, QuoteRequest, Service


INPUT_CLASS = 'field-input'
SELECT_CLASS = 'field-input'
TEXTAREA_CLASS = 'field-input field-textarea'


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Your full name',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'you@company.com',
                'autocomplete': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': '+91 98765 43210',
                'autocomplete': 'tel',
            }),
            'subject': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'How can we help?',
            }),
            'message': forms.Textarea(attrs={
                'class': TEXTAREA_CLASS,
                'placeholder': 'Tell us about your business and what you need.',
                'rows': 5,
            }),
        }


class QuoteForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = [
            'name',
            'email',
            'phone',
            'company',
            'service',
            'budget',
            'timeline',
            'project_details',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Your full name',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'you@company.com',
                'autocomplete': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': '+91 98765 43210',
                'autocomplete': 'tel',
            }),
            'company': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Business name',
            }),
            'service': forms.Select(attrs={'class': SELECT_CLASS}),
            'budget': forms.Select(attrs={'class': SELECT_CLASS}),
            'timeline': forms.Select(attrs={'class': SELECT_CLASS}),
            'project_details': forms.Textarea(attrs={
                'class': TEXTAREA_CLASS,
                'placeholder': 'Describe the website you want, pages, features, and any examples you like.',
                'rows': 6,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.all()
        self.fields['service'].empty_label = 'Select a service'
        self.fields['service'].required = False
        self.fields['budget'].required = True
        self.fields['timeline'].required = True
