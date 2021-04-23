from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class AccountActivateGeneratorToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.profile.email_confirmed)
        )
api_account_activate_token = AccountActivateGeneratorToken()