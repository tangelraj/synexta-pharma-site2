import json
import tempfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail
from django.test import TestCase
from django.test import override_settings
from PIL import Image

from .models import ContactInquiry, Product, SiteContent, SiteContentItem


class SiteContentApiTests(TestCase):
    def test_site_content_admin_list_page_renders(self):
        from django.contrib.auth import get_user_model
        from django.urls import reverse

        user = get_user_model().objects.create_superuser(
            username="content-admin",
            email="admin@example.com",
            password="Admin-Test-Password-482!",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("admin:inquiries_sitecontent_changelist"))

        self.assertEqual(response.status_code, 200)

    def test_returns_editable_site_content(self):
        content = SiteContent.objects.get(pk="default")
        content.about_title = "Updated about heading"
        content.save()

        response = self.client.get("/api/content/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["about_title"], "Updated about heading")
        self.assertEqual(response.json()["nav_links"][0]["label"], "Home")
        self.assertIn("hero_image", response.json())
        self.assertIsNone(response.json()["hero_image"])

    def test_returns_individually_editable_content_items(self):
        response = self.client.get("/api/content/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nav_links"][0], {"label": "Home", "href": "#home"})
        self.assertEqual(
            response.json()["about_points"][0],
            {
                "icon": "care",
                "title": "Quality-Focused Approach",
                "text": "Every Formulation is presented with care, clarity and consistency.",
            },
        )
        self.assertEqual(response.json()["footer_legal_links"][0], {"label": "Privacy Policy"})

        nav_link = SiteContentItem.objects.get(
            section=SiteContentItem.Section.NAV_LINK,
            sort_order=0,
        )
        nav_link.label = "Home page"
        nav_link.save()
        updated_response = self.client.get("/api/content/")
        self.assertEqual(updated_response.json()["nav_links"][0]["label"], "Home page")

    def test_site_content_admin_displays_row_editors(self):
        from django.contrib.auth import get_user_model
        from django.urls import reverse

        user = get_user_model().objects.create_superuser(
            username="content-admin",
            email="admin@example.com",
            password="test-password",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("admin:inquiries_sitecontent_change", args=("default",)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Navigation links")
        self.assertContains(response, "About points")
        self.assertContains(response, "Footer quick links")
        self.assertContains(response, "name=\"items-0-label\"")

    def test_rejects_non_get_method(self):
        response = self.client.post("/api/content/")

        self.assertEqual(response.status_code, 405)

    def test_returns_uploaded_site_and_product_image_urls(self):
        image_buffer = BytesIO()
        Image.new("RGB", (1, 1)).save(image_buffer, format="PNG")
        image_data = image_buffer.getvalue()

        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                content = SiteContent.objects.get(pk="default")
                content.hero_image.save(
                    "hero.png",
                    SimpleUploadedFile("hero.png", image_data, content_type="image/png"),
                )
                product = Product.objects.first()
                product.image.save(
                    "product.png",
                    SimpleUploadedFile("product.png", image_data, content_type="image/png"),
                )

                content_response = self.client.get("/api/content/")
                products_response = self.client.get("/api/products/")

        self.assertEqual(content_response.json()["hero_image"], "/media/site/hero.png")
        self.assertTrue(products_response.json()["products"][0]["image"].startswith("/media/products/"))


class ProductApiTests(TestCase):
    def test_lists_products(self):
        response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["products"]), 7)
        self.assertEqual(response.json()["products"][0]["id"], "neurosyn-m")
        self.assertIn("image", response.json()["products"][0])

    def test_rejects_non_get_method(self):
        response = self.client.post("/api/products/")

        self.assertEqual(response.status_code, 405)


class ContactApiTests(TestCase):
    def test_saves_valid_contact_inquiry(self):
        payload = {
            "name": "Avery Example",
            "email": "avery@example.com",
            "phone": "+1 555 010 0200",
            "topic": "Product enquiry",
            "message": "I would like to learn more about your product portfolio.",
        }

        with override_settings(
            EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
            EMAIL_HOST_USER="sender@example.com",
            EMAIL_HOST_PASSWORD="test-password",
            DEFAULT_FROM_EMAIL="sender@example.com",
            INQUIRY_NOTIFICATION_EMAIL="tangelraj@gmail.com",
        ):
            response = self.client.post(
                "/api/contact/",
                data=json.dumps(payload),
                content_type="application/json",
            )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["email_sent"])
        self.assertEqual(ContactInquiry.objects.count(), 1)
        self.assertEqual(ContactInquiry.objects.get().email, payload["email"])
        self.assertEqual(ContactInquiry.objects.get().company, "")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["tangelraj@gmail.com"])
        self.assertIn(payload["message"], mail.outbox[0].body)

    def test_saves_inquiry_but_reports_when_email_is_not_configured(self):
        payload = {
            "name": "Avery Example",
            "email": "avery@example.com",
            "phone": "+1 555 010 0200",
            "company": "Example Health",
            "topic": "Business enquiry",
            "message": "I would like to discuss a business partnership.",
        }

        with override_settings(EMAIL_HOST_USER="", EMAIL_HOST_PASSWORD=""):
            response = self.client.post(
                "/api/contact/",
                data=json.dumps(payload),
                content_type="application/json",
            )

        self.assertEqual(response.status_code, 202)
        self.assertFalse(response.json()["email_sent"])
        self.assertEqual(ContactInquiry.objects.count(), 1)
        self.assertEqual(ContactInquiry.objects.get().company, payload["company"])

    def test_rejects_invalid_email(self):
        response = self.client.post(
            "/api/contact/",
            data=json.dumps({"name": "Avery", "email": "not-an-email", "topic": "General", "message": "A long enough message."}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.json()["errors"])
        self.assertEqual(ContactInquiry.objects.count(), 0)

    def test_rejects_malformed_json(self):
        response = self.client.post("/api/contact/", data="{", content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_rejects_non_json_content_type(self):
        response = self.client.post("/api/contact/", data="name=Avery", content_type="text/plain")

        self.assertEqual(response.status_code, 415)