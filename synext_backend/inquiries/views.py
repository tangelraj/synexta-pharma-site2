import json
import logging
import smtplib

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import ContactInquiry, Product, SiteContent, SiteContentItem


logger = logging.getLogger(__name__)


@require_GET
def site_content(request):
    content = SiteContent.objects.first()
    if content is None:
        return JsonResponse({"error": "Website content has not been configured."}, status=503)

    fields = (
        "logo_image",
        "hero_image",
        "about_image",
        "quality_background_image",
        "why_image",
        "contact_background_image",
        "nav_cta_label",
        "nav_cta_href",
        "about_eyebrow",
        "about_title",
        "about_body",
        "quality_eyebrow",
        "commitments_title",
        "commitments_subtitle",
        "why_eyebrow",
        "why_title",
        "why_body",
        "footer_tagline",
        "footer_products_heading",
        "footer_copyright",
    )
    data = {field: getattr(content, field) for field in fields if not field.endswith("_image")}
    data.update({
        field: getattr(content, field).url if getattr(content, field) else None
        for field in fields
        if field.endswith("_image")
    })
    item_fields = {
        "nav_links": (SiteContentItem.Section.NAV_LINK, ("label", "href")),
        "about_points": (SiteContentItem.Section.ABOUT_POINT, ("icon", "title", "text")),
        "quality_points": (SiteContentItem.Section.QUALITY_POINT, ("icon", "title", "text")),
        "commitments_points": (SiteContentItem.Section.COMMITMENT_POINT, ("icon", "title", "text")),
        "why_points": (SiteContentItem.Section.WHY_POINT, ("icon", "title", "text")),
        "footer_quick_links": (SiteContentItem.Section.FOOTER_QUICK_LINK, ("label", "href")),
        "footer_product_links": (SiteContentItem.Section.FOOTER_PRODUCT_LINK, ("label", "href")),
        "footer_legal_links": (SiteContentItem.Section.FOOTER_LEGAL_LINK, ("label", "href")),
    }
    items = content.items.order_by("sort_order", "pk")
    for output_field, (section, item_keys) in item_fields.items():
        data[output_field] = [
            {
                key: getattr(item, key)
                for key in item_keys
                if key != "href" or item.href
            }
            for item in items
            if item.section == section
        ]
    return JsonResponse(data)


@require_GET
def products(request):
    catalogue = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "category": product.category,
            "image": product.image.url if product.image else None,
        }
        for product in Product.objects.all()
    ]
    return JsonResponse({"products": catalogue})


@csrf_exempt
@require_POST
def contact(request):
    if request.content_type != "application/json":
        return JsonResponse({"error": "Content-Type must be application/json."}, status=415)

    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Request body must contain valid JSON."}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({"error": "Request body must be a JSON object."}, status=400)

    fields = {
        "name": str(payload.get("name", "")).strip(),
        "email": str(payload.get("email", "")).strip(),
        "phone": str(payload.get("phone", "")).strip(),
        "company": str(payload.get("company", "")).strip(),
        "topic": str(payload.get("topic", "")).strip(),
        "message": str(payload.get("message", "")).strip(),
    }
    errors = {}

    for field, value in fields.items():
        if field in {"name", "email", "topic", "message"} and not value:
            errors[field] = "This field is required."

    limits = {"name": 120, "email": 254, "phone": 30, "company": 120, "topic": 120, "message": 5000}
    for field, limit in limits.items():
        if len(fields[field]) > limit:
            errors[field] = f"This field must be {limit} characters or fewer."

    if fields["message"] and len(fields["message"]) < 10:
        errors["message"] = "Please enter at least 10 characters."

    if fields["email"]:
        try:
            validate_email(fields["email"])
        except ValidationError:
            errors["email"] = "Enter a valid email address."

    if errors:
        return JsonResponse({"errors": errors}, status=400)

    inquiry = ContactInquiry.objects.create(**fields)
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        logger.error("Contact inquiry %s was saved, but SMTP credentials are not configured.", inquiry.pk)
        return JsonResponse(
            {
                "id": inquiry.pk,
                "email_sent": False,
                "message": "Your enquiry was saved, but the notification email could not be sent because SMTP is not configured.",
            },
            status=202,
        )

    email_body = "\n".join(
        (
            "A new website enquiry has been submitted.",
            "",
            f"Name: {inquiry.name}",
            f"Email: {inquiry.email}",
            f"Phone: {inquiry.phone or 'Not provided'}",
            f"Company: {inquiry.company or 'Not provided'}",
            f"Enquiry type: {inquiry.topic}",
            "",
            "Message:",
            inquiry.message,
        )
    )
    try:
        email = EmailMessage(
            subject="New Synexta Pharma website enquiry",
            body=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.INQUIRY_NOTIFICATION_EMAIL],
            reply_to=[inquiry.email],
        )
        sent_count = email.send(fail_silently=False)
    except (OSError, smtplib.SMTPException, ValueError) as error:
        logger.exception("Could not email contact inquiry %s.", inquiry.pk)
        return JsonResponse(
            {
                "id": inquiry.pk,
                "email_sent": False,
                "message": "Your enquiry was saved, but the notification email could not be sent. Please contact us directly.",
            },
            status=202,
        )

    if sent_count != 1:
        logger.error("Email backend did not send contact inquiry %s.", inquiry.pk)
        return JsonResponse(
            {
                "id": inquiry.pk,
                "email_sent": False,
                "message": "Your enquiry was saved, but the notification email could not be sent. Please contact us directly.",
            },
            status=202,
        )

    return JsonResponse(
        {
            "id": inquiry.pk,
            "email_sent": True,
            "message": "Your message has been received. Thank you for reaching out.",
        },
        status=201,
    )