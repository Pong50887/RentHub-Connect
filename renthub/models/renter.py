from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator


class Renter(User):
    """
    Represents a renter, extending Django's default User model.
    """
    phone_number = models.CharField(max_length=10,
                                    validators=[
                                        RegexValidator(
                                            regex=r'^\d{10}$',
                                            message="Phone number must be exactly 10 digits."
                                        )
                                    ])
    thai_citizenship_id = models.CharField(max_length=13, blank=True, null=True, unique=True)

    class Meta:
        verbose_name = "Renter"
        verbose_name_plural = "Renters"

    def __str__(self):
        """Returns the username of the renter."""
        return self.username
