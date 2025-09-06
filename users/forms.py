from django import forms
from .models import TaxDocument

class TaxDocumentForm(forms.ModelForm):
    class Meta:
        model = TaxDocument
        fields = ["client", "document"]

    # Optional: size/type validation (matches your hint text)
    def clean_document(self):
        f = self.cleaned_data["document"]
        if f.size > 10 * 1024 * 1024:
            raise forms.ValidationError("File too large (max 10MB).")
        allowed = (".pdf", ".jpg", ".jpeg", ".png", ".docx", ".xlsx")
        if not any(f.name.lower().endswith(ext) for ext in allowed):
            raise forms.ValidationError("Unsupported file type.")
        return f
