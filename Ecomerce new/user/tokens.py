from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

# class UserTokenGenration(PasswordResetTokenGenerator):
#     def _make_hash_value(self,user, timestamp):
#         user_id = six.text_type(user.pk)
#         ts = six.text_type(timestamp)
#         is_active = six.text_type(user.is_active)
#         return f"{user_id}{ts}{is_active}"
    
# user_tokenizer = UserTokenGenration()

class AccountActivateGeneratorToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.profile.email_confirmed)
        )
account_activate_token = AccountActivateGeneratorToken()