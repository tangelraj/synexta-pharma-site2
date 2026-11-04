import os

from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create an initial admin from environment variables if the account does not exist."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")
        supplied_values = (username, email, password)

        if not any(supplied_values):
            self.stdout.write("Admin bootstrap is not configured; skipping.")
            return
        if not all(supplied_values):
            raise CommandError(
                "Set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, "
                "and DJANGO_SUPERUSER_PASSWORD together."
            )

        user_model = get_user_model()
        existing_user = user_model._default_manager.filter(username=username).first()
        if existing_user is not None:
            if not (existing_user.is_staff and existing_user.is_superuser):
                raise CommandError(
                    "The configured admin username already belongs to a non-admin account. "
                    "Choose a different DJANGO_SUPERUSER_USERNAME."
                )
            self.stdout.write("The configured admin already exists; no changes made.")
            return

        user = user_model(username=username, email=email)
        try:
            password_validation.validate_password(password, user=user)
        except ValidationError as error:
            raise CommandError("; ".join(error.messages)) from error

        user_model._default_manager.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(self.style.SUCCESS("Initial admin account created."))
