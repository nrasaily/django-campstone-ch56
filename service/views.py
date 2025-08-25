from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Service, Payment

from pages.models import Client 
from django.contrib import messages
import stripe
from django.conf import settings

from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

def service_list(request):
    services = Service.objects.filter(is_active=True)
    return render(request, "service/service.html", {"services": services})


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    return render(request, "service/service_detail.html", {"service": service})


@login_required
def service_pay(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    
    # Find logged in user's Client profile
    client, _ = Client.objects.get_or_create(user=request.user) # avoid 404

    #Init stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY


    # Build abbsolute urls for success/cancel
    success_url = request.build_absolute_uri(
        reverse("service:payment_success")
    )+ "?session_id={CHECKOUT_SESSION_ID}"
    cancel_url = request.build_absolute_uri(
        reverse("service:payment_cancel")
    )


    # Pick a readable product name
    product_name = getattr(service, "title", None) or getattr(service, "name", None) or str(service)

    # Create checkout session
    try:
      checkout_session = stripe.checkout.Session.create(
          mode="payment",
          line_items=[{
              "price_data": {
                  "currency": "usd",
                  "product_data": {"name": product_name},
                  "unit_amount": int(service.price * 100), # cents
              },
              "quantity": 1,
          }],
          customer_email=request.user.email or None,
          success_url=success_url,
          cancel_url=cancel_url,
          metadata={
              "django_user_id": str(request.user.id),
              "service_slug": service.slug,
          },
      )
    
      
    
      
    
    except stripe.error.StripeError as e:
      logger.error(f"Stripe error: {str(e)}")
      messages.error(request, f"Stripe error: {str(e)}")
      return redirect("service:detail", slug=slug)


    # Save pending payment in your DB (note: don't shadow the model name)
    payment = Payment.objects.create(
        client=client,
        service=service,
        amount=service.price,
        currency="USD",
        method="card", # or "cash" if you prefer
        status="pending", # you can set success if you want to simulate success
        reference=checkout_session.id,  # store stripe session id
    )

    # Optionally show a flash before redirect

    messages.info(request, "Redirecting to secure Stripe checkout...")
    return redirect(checkout_session.url, permanent=False)


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