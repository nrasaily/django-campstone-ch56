from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_profile")
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class TaxDocument(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="documents")
    document_name = models.CharField(max_length=200)
    document_file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_name} — {self.client.full_name}"


class TaxFiling(models.Model):
    INDIVIDUAL = "individual"
    BUSINESS = "business"
    FILING_TYPES = [(INDIVIDUAL, "Individual"), (BUSINESS, "Business")]

    PENDING = "pending"
    IN_REVIEW = "in_review"
    FILED = "filed"
    STATUSES = [(PENDING, "Pending"), (IN_REVIEW, "In Review"), (FILED, "Filed")]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="filings")
    year = models.PositiveIntegerField()
    filing_type = models.CharField(max_length=100, choices=FILING_TYPES)
    status = models.CharField(max_length=50, choices=STATUSES, default=PENDING)
    submitted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.client.full_name} — {self.year} — {self.filing_type}"


class Consultation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="consultations")
    date = models.DateTimeField()
    topic = models.CharField(max_length=200)
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.full_name} — {self.date.strftime('%Y-%m-%d')}"
