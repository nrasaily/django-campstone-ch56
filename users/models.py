from django.db import models

class Client(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.full_name

def doc_upload_path(instance, filename):
    # media/docs/2025/09/yourfile.pdf (folders auto-created)
    return f"docs/{instance.created_at:%Y/%m}/{filename}"

class TaxDocument(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="documents")
    document = models.FileField(upload_to=doc_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)
