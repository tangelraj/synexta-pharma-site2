import os
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command, CommandError
from django.test import TestCase


class BootstrapAdminCommandTests(TestCase):
    def test_skips_when_environment_is_not_configured(self):
        with patch.dict(os.environ, {}, clear=False):
            for key in (
                "DJANGO_SUPERUSER_USERNAME",
                "DJANGO_SUPERUSER_EMAIL",
                "DJANGO_SUPERUSER_PASSWORD",
            ):
                os.environ.pop(key, None)

            call_command("bootstrap_admin")

        self.assertEqual(get_user_model().objects.count(), 0)

    def test_requires_all_environment_values(self):
        with patch.dict(
            os.environ,
            {
                "DJANGO_SUPERUSER_USERNAME": "site-admin",
                "DJANGO_SUPERUSER_EMAIL": "",
                "DJANGO_SUPERUSER_PASSWORD": "",
            },
        ):
            with self.assertRaisesMessage(CommandError, "Set DJANGO_SUPERUSER_USERNAME"):
                call_command("bootstrap_admin")

        self.assertEqual(get_user_model().objects.count(), 0)

    def test_creates_admin_from_environment(self):
        with patch.dict(
            os.environ,
            {
                "DJANGO_SUPERUSER_USERNAME": "site-admin",
                "DJANGO_SUPERUSER_EMAIL": "admin@example.com",
                "DJANGO_SUPERUSER_PASSWORD": "A-Long-Random-Password-938!",
            },
        ):
            call_command("bootstrap_admin")

        admin = get_user_model().objects.get(username="site-admin")
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.check_password("A-Long-Random-Password-938!"))

    def test_existing_admin_password_is_not_changed(self):
        user_model = get_user_model()
        admin = user_model.objects.create_superuser(
            username="site-admin",
            email="admin@example.com",
            password="Original-Password-938!",
        )

        with patch.dict(
            os.environ,
            {
                "DJANGO_SUPERUSER_USERNAME": "site-admin",
                "DJANGO_SUPERUSER_EMAIL": "admin@example.com",
                "DJANGO_SUPERUSER_PASSWORD": "A-Different-Password-482!",
            },
        ):
            call_command("bootstrap_admin")

        admin.refresh_from_db()
        self.assertTrue(admin.check_password("Original-Password-938!"))
        self.assertFalse(admin.check_password("A-Different-Password-482!"))
