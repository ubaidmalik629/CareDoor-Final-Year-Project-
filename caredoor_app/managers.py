from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, password=None, **extra_fields):
        email = extra_fields['email']
        if not email:
            raise ValueError("The Email field must be set.")
        email = self.normalize_email(email)
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, password=None, **extra_fields):
        extra_fields.setdefault("age", 18)
        extra_fields.setdefault("contact", 123456789)
        extra_fields.setdefault("gender", "M")
        extra_fields.setdefault("user_type", "A")
        extra_fields.setdefault("address", "login")
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)
