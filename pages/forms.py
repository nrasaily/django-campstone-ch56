from django import forms
from .models import TaxDocument

class TaxDocumentForm(forms.ModelForm):
  class Meta:
    model =TaxDocument
    fields = ['client', 'document_file']


class ContactForm(forms.Form):
  name = forms.CharField(max_length=100, label="Your Name")
  email = forms.EmailField(label="Your Email")
  message = forms.CharField(widget=forms.Textarea, label="Your Message")