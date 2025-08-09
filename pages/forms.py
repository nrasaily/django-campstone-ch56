from django import forms
from .models import TaxDocument

class TaxDocumentForm(forms.ModelForm):
  class Meta:
    model =TaxDocument
    fields = ['client', 'document_file']