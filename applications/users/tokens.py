import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# Token generator for user account activation.
class TokenGenerator(PasswordResetTokenGenerator):
    """Token generator for user account activation."""

    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()
