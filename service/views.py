from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Service, Payment

from pages.models import Client 
from django.contrib import messages
import stripe
from django.conf import settings

from django.urls import reverse
import logging
import stripe 

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

def service_list(request):
    services = Service.objects.filter(is_active=True)
    return render(request, "service/service.html", {"services": services})


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    return render(request, "service/service_detail.html", {"service": service})


@login_required
def service_pay(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    return render(request, "service/payment_form.html", {"service": service})


    


    
    
      
    
    
import stripe

def payment_success(request):
    session_id = request.GET.get("session_id")
    if session_id:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)
        # Optionally update payment status here
    messages.success(request, "Payment successful! 🎉")
    return render(request, "service/payment_success.html")


def payment_cancel(request):
    messages.warning(request, "Payment canceled.")
    return render(request, "service/payment_cancel.html")

from django.urls import reverse
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def process_payment(request, slug):
    if request.method != "POST":
        return redirect("service:pay", slug=slug)

    service = get_object_or_404(Service, slug=slug, is_active=True)
    full_name = request.POST.get("full_name", "").strip()
    receipt_email = request.POST.get("email", "").strip()

    success_url = request.build_absolute_uri(
        reverse("service:payment_success")
    ) + "?session_id={CHECKOUT_SESSION_ID}"
    cancel_url = request.build_absolute_uri(reverse("service:payment_cancel"))

    # Create Stripe checkout session
    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "unit_amount": int(service.price * 100),  # cents
                "product_data": {"name": service.title},
            },
            "quantity": 1,
        }],
        customer_email=receipt_email or None,  # OK if blank
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "service_slug": service.slug,
            "service_title": service.title,
            "buyer_name": full_name,
            "buyer_email": receipt_email,
        },
    )
    return redirect(session.url, code=303)
