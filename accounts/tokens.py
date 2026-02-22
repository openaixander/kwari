from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils.six  # Django usually bundles this, or use 'django.utils.six' if available, or just str() in Py3

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # We only hash the PK, the timestamp, and the is_active state.
        # If the user is already active, the hash changes (invalidating the old link).
        return (
            str(user.pk) + str(timestamp) + str(user.is_active)
        )

# Singleton instance
account_activation_token = AccountActivationTokenGenerator()