
from django.db import models
from django.urls import reverse

# Use string FKs to avoid circular imports
# ('app_label.ModelName' style)
class Service(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("service:detail", args=[self.slug])

    def pay_url(self):
        return reverse("service:pay", args=[self.slug])


class Payment(models.Model):
    client = models.ForeignKey("pages.Client", on_delete=models.CASCADE, related_name="payments")
    service = models.ForeignKey("service.Service", on_delete=models.CASCADE, related_name="payments")
    consultation = models.ForeignKey(
        "pages.Consultation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )
    tax_filing = models.ForeignKey(
        "pages.TaxFiling",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="USD")
    method = models.CharField(
        max_length=20,
        choices=[("cash", "Cash"), ("card", "Card"), ("paypal", "PayPal"), ("bank", "Bank Transfer")],
    )
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("completed", "Completed"), ("failed", "Failed"), ("refunded", "Refunded")],
        default="pending",
    )
    reference = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.full_name} — {self.amount} {self.currency} ({self.status})"
