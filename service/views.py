from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import Service, Payment

from pages.models import Client 
from django.contrib import messages
import stripe
from django.conf import settings

from django.urls import reverse
import logging
import stripe 
from django.views.decorators.http import require_POST

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


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


"""

uSer clicks on pay
process_payment is called, it send to stripe page
user pays

stripe_webhook (never called, logic to send email is here)

payment_success is called

"""

@login_required
def process_payment(request, slug):
    print("process_payment")
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
        customer_email=receipt_email,  # OK if blank
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "service_slug": service.slug,
            "service_title": service.title,
            "buyer_name": full_name,
            "buyer_email": receipt_email,
            "user_id": str(request.user.id),
        },
    )
    return redirect(session.url, code=303)

@csrf_exempt
def stripe_webhook(request):
    
    if request.method == "GET":
        print("Webhook with get")
        return "TEST"

    print("Step 1")
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    endpoint_secret = getattr(settings, "STRIPE_WEBHOOK_SECRET", None)

    try:
      event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        print("Invalid payload:", e)
        return HttpResponse(status=400) # invalid payload
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400) # invalid signature
    
    print("Step 2: event type =", event.get("type"))
    # Fire when the Checkout flow complete successfully
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print("Payment success for", session.get("id"))

      # Who to email
        to_email = (session.get("customer_details") or {}).get("email") \
                    or session.get("customer_email") \
                    or (session.get("metadata") or {}).get("buyer_email")

        print("Webhook resolved to_email =", to_email)

          #Useful details
        amount_total = (session.get("amount_total") or 0)/ 100.0
        currency = (session.get("currency") or "usd").upper()
        service_slug = (session.get("metadata")or {}).get("service_slug")
        service_title = (session.get("metadata") or {}).get("service_title")
        buyer_name = (session.get("metadata") or {}).get("buyer_name")

        # (Optional) Update your Payment model here if desired
        try:
            client = Client.objects.get(user__email=to_email)
            Payment.objects.create(
                client=client,
                amount=amount_total,
                currency=currency,
                method="card",
                status="paid",
                reference=session.get("id"),
            )
        except Client.DoesNotExist:
            print("Client not found for", to_email)
    
    

        #Send email (only if we have an email)
        if to_email:
            print("Step 4: sending email to", to_email)
            context = {
                "buyer_name": buyer_name,
                "service_title": service_title,
                "amount": f"{amount_total:.2f}",
                "currency": currency,
                "session_id": session.get("id"),
            }
            subject = "Payment recieved - thank you"
            from_email = settings.DEFAULT_FROM_EMAIL
            text_body = render_to_string("emails/payment_success.txt", context)
            html_body = render_to_string("emails/payment_success.html", context)

            msg = EmailMultiAlternatives(subject, text_body, from_email, [to_email])
            msg.attach_alternative(html_body, "text/html")
            msg.send(fail_silently=False)
            print("Step 5: email sent")

    print("Step 6: 200 OK")
    return HttpResponse(status=200)